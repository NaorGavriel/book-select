from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud.jobs import get_job_by_id, update_job_status
from app.models.enums import JobStatus
from app.celery_app import celery_app
import time
from app.storage.storage_factory import get_storage_backend
from app.crud.job_results import create_job_result
from app.services.books.resolver import resolve_books
from app.services.ocr.ocr import extract_books_from_image
from app.services.scoring.scoring import get_best_similarity, score_book
from app.dto.book_result import BookResult

@celery_app.task
def process_job(job_id: int):
    """
    Execute an image-processing job.

    Updates job status as it progresses and records failure details
    if an exception occurs.
    """
    db: Session = SessionLocal()
    job = None

    try:
        job = get_job_by_id(db, job_id)
        if job is None:
            return

        if job.status != JobStatus.pending: # preventing double-exec of the job by checking status
            return

        update_job_status(db, job, status=JobStatus.processing)
        storage = get_storage_backend()

        image_bytes = storage.load_image(key=job.image_path)

        detected_books = extract_books_from_image(image_bytes)

        resolved_books = resolve_books(db, detected_books)

        for candidate in resolved_books:
            most_similar_book, similarity = get_best_similarity(db=db, candidate=candidate, user_id=job.user_id)
            book_result = score_book(candidate=candidate, user_id=job.user_id, similarity=similarity, similar_book=most_similar_book)
            create_job_result(db=db, book_result=book_result, job_id=job_id)

        db.commit()
        update_job_status(db, job, status=JobStatus.completed)

    except Exception as e:
        db.rollback()
        if job is not None:
            update_job_status(db, job, status=JobStatus.failed, error_message=str(e))
        raise

    finally:
        db.close()
