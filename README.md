# BookSelect
BookSelect is a full-stack web application that helps users choose what to read by analyzing bookshelf photos and generating personalized recommendations based on their reading history.

The system extracts book titles from uploaded bookshelf images using OCR, enriches them with metadata from the Google Books API, and generates recommendations using semantic similarity search based on vector embeddings.

## Screenshots

<p align="center">
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/reading-history-screenshot.png?raw=true" width="25%" />
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/upload-image-screenshot2.png?raw=true" width="25%" />
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/results-screenshot.png?raw=true" width="25%" />
</p>

## Prerequisites
- Docker (Docker Desktop)
- OpenAI API key
- Google Books API key
- Git

## Installation & Running the Application
1. Clone the repository :
```
git clone https://github.com/NaorGavriel/book-select.git
cd book-select
```
2. Create a .env file in the project root:
```
cp .env.example .env
```
3. Start backend, frontend, database, and Redis services :
```
docker compose up --build
```
4. In a separate terminal (from the project root directory), apply database migrations:
```
docker compose exec api alembic upgrade head
```  
5. Access the application at :
   ```http://localhost:5173```

## Environment Variables
Create a `.env` file in the project root and fill in the required variables.
You can use the provided template:

```
cp .env.example .env
```

## Features
- Extracts book titles from uploaded bookshelf images using OCR
- Generates personalized book recommendations using semantic similarity search based on reading history
- Enriches detected books with metadata (authors, description, categories)
- Asynchronous background processing using Celery and Redis
- Secure authentication with JWT
- API rate limiting to prevent abuse

## Usage
1. Open the application at `http://localhost:5173`.
2. Register an account and log in.
3. Add books you enjoy to your reading history.
4. Snap a photo of a bookshelf (ensure book spines are clearly visible).
5. Upload the image to the application.
6. View personalized recommendations.

## Database Migrations

After modifying SQLAlchemy models, create a new migration from the project root directory:
```
docker compose exec api alembic revision --autogenerate -m "describe your change"
```
Then apply the migration:
```
docker compose exec api alembic upgrade head
```
