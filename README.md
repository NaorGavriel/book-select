# BookSelect
BookSelect is a full-stack web application that helps users choose what to read by analyzing bookshelf photos and generating personalized recommendations based on their reading history.

The system extracts book titles from uploaded bookshelf images using OCR, enriches them with metadata from the Google Books API, and generates recommendations using semantic similarity search based on vector embeddings.

## Screenshots

<p align="center">
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/reading-history-screenshot.png?raw=true" width="25%" />
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/upload-image-screenshot2.png?raw=true" width="25%" />
   <img src="https://github.com/NaorGavriel/book-select/blob/main/screenshots/results-screenshot.png?raw=true" width="25%" />
</p>

## Architecture

BookSelect is built as a distributed system with asynchronous job processing,
designed to handle the latency of OCR and external API calls without blocking
the user.

### System overview

![Architecture diagram](./docs/bookselect-system-architecture.svg)

The backend is split between a **FastAPI** server handling HTTP requests and
**Celery workers** processing scan jobs asynchronously. **Redis** acts as the
message broker between them. **PostgreSQL** stores users, reading history,
job results, and a cache of book metadata fetched from the Google
Books API.

### AWS deployment

Deployed on AWS with the following setup:

- **CloudFront + S3** serve the React frontend globally
- **ECS Fargate** runs FastAPI and Celery workers
- **Application Load Balancer** distributes traffic across two availability zones
- **RDS PostgreSQL** (multi-AZ) and **ElastiCache Redis** handle data persistence
  and job queuing in a private data subnet
- A **VPC endpoint** routes S3 traffic privately without going through the NAT gateway
- A single **NAT gateway** in AZ-a handles outbound calls to the OCR model and
  Google Books API

For the detailed request flow of the bookshelf scan feature, see
[docs/sequence-scan-feature.md](./docs/bookshelf_scan_feature_squence.md).

## Prerequisites
- Docker (Docker Desktop)
- OpenAI API key
- Google Books API key
- Git

## Installation & Running the Application
1. Clone the repository & navigate to the project root directory:
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
   
## Features

- Bookshelf scanning via OCR with personalized recommendations based on reading history
- Semantic similarity search using vector embeddings
- Asynchronous background processing (Celery + Redis)
- Secure authentication with JWT
- API rate limiting
- Admin dashboard with protected endpoints

## Usage

1. Open the application at `http://localhost:5173`.
2. Register an account and log in.
3. Add books you enjoy to your reading history.
4. Snap a photo of a bookshelf (ensure book spines are clearly visible).
5. Upload the image to the application.
6. View personalized recommendations.

## Admin Access

After registering a normal account, promote the user to admin from the project root directory:
```
docker compose exec api python -m scripts.promote_user user@example.com
```
Admin users can access the operational dashboard and protected admin endpoints.

## Database Migrations

After modifying SQLAlchemy models, create a new migration from the project root directory:
```
docker compose exec api alembic revision --autogenerate -m "describe your change"
```
Then apply the migration:
```
docker compose exec api alembic upgrade head
```
