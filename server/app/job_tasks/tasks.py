from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud.jobs import get_job_by_id, update_job_status
from app.models.enums import JobStatus
from app.celery_app import celery_app
from app.storage.storage_factory import get_storage_backend
from app.crud.job_results import create_job_result
from app.services.books.resolver import resolve_books
from app.services.ocr.ocr import extract_books_from_image
from app.services.scoring.scoring import get_best_similarity, score_book
import logging
from app.core.config import GeneralConfig

logger = logging.getLogger(GeneralConfig.API_LOGGER_NAME)

@celery_app.task
def process_job(job_id: int, user_id: int):
    """
    Process a single book-detection job asynchronously.

    Workflow:
        1. Load image from storage.
        2. Run OCR to detect books.
        3. Resolve detected books against the database.
        4. Compute similarity scores and persist results.

    Args:
        job_id (int): Identifier of the job to process.
    """
    db: Session = SessionLocal()
    job = None

    try:
        job = get_job_by_id(user_id=user_id, job_id=job_id, db=db)
        if job is None:
            return

        if job.status != JobStatus.pending: # preventing double-exec of the job by checking status
            return

        
        update_job_status(db, job, status=JobStatus.processing)
        logger.info(f"job {job_id} processing")
        storage = get_storage_backend()

        
        image_bytes = storage.load_image(key=job.image_path) # Load image from storage backend
        detected_books = extract_books_from_image(image_bytes) # Extract raw book candidates from image
        resolved_books = resolve_books(db, detected_books) # Resolve OCR output into structured book candidates

        for candidate in resolved_books:
            # Score each resolved candidate against user's reading history
            most_similar_book, similarity = get_best_similarity(db=db, candidate=candidate, user_id=job.user_id)
            book_result = score_book(candidate=candidate, user_id=job.user_id, similarity=similarity, similar_book=most_similar_book)
            create_job_result(db=db, book_result=book_result, job_id=job_id)

        db.commit()
        update_job_status(db, job, status=JobStatus.completed)
        logger.info(f"job {job_id} completed")

    except Exception as e:
        db.rollback() # Roll back DB changes on failure
        if job is not None:
            update_job_status(db, job, status=JobStatus.failed, error_message=str(e))
            logger.info(f"job {job_id} failed")
        raise

    finally:
        db.close()
