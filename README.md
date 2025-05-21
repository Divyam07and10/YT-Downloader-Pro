YouTube Video Downloader
A production-grade FastAPI application for downloading YouTube videos asynchronously using Celery, storing metadata in PostgreSQL, and uploading videos to S3 (with a mock S3 implementation). The application supports video and audio formats, quality selection, and robust error handling with a fallback to pytube if yt-dlp fails.
Features

Asynchronous Downloads: Uses Celery with Redis for background video downloading.
Format and Quality Options: Supports mp4, webm, mkv, and mp3 formats with qualities (360p, 480p, 720p, 1080p, 4k).
Fallback Mechanism: If yt-dlp fails, retries with pytube (up to 2 attempts).
Database Storage: Stores video metadata in PostgreSQL using SQLAlchemy.
S3 Integration: Uploads videos to a mock S3 bucket using boto3 and moto.
Database Migrations: Manages schema changes with Alembic.
Production-Grade Architecture: Modular design with clear separation of concerns (API, tasks, database, utilities).

Tech Stack

Backend: FastAPI, Python 3.12
Task Queue: Celery with Redis
Database: PostgreSQL with SQLAlchemy (async and sync)
Downloader: yt-dlp (primary), pytube (fallback)
Storage: Mock S3 (via moto)
Migrations: Alembic
Dependencies: Managed via requirements.txt

Prerequisites

Python: 3.12 or higher
Redis: For Celery task queue
PostgreSQL: For metadata storage
FFmpeg: Required for MP3 conversion
Virtual Environment: Recommended for dependency isolation

Setup Instructions
1. Clone the Repository
git clone https://github.com/your-repo/youtube-downloader.git
cd youtube-downloader

2. Create and Activate Virtual Environment
python -m venv yt
source yt/bin/activate  # On Windows: yt\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Install System Dependencies

Redis (Ubuntu):sudo apt-get install redis-server
redis-server  # Start Redis


PostgreSQL (Ubuntu):sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start


FFmpeg (Ubuntu):sudo apt-get install ffmpeg



5. Configure Environment Variables
Create a .env file in the project root with the following:
REDIS_URL=redis://localhost:6379/0
DB_HOST=localhost
DB_PORT=5432
DB_NAME=youtube
DB_USER=your_db_user
DB_PASSWORD=your_db_password
S3_BUCKET=my-youtube-videos
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

Load the environment variables:
export $(cat .env | xargs)

6. Set Up PostgreSQL Database
Create the database and user:
sudo -u postgres psql
CREATE DATABASE youtube;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE youtube TO your_db_user;
\q

7. Apply Database Migrations
Initialize the database schema using Alembic:
alembic upgrade head

8. Verify Setup

Check Redis: redis-cli ping (should return PONG)
Check PostgreSQL: psql -h localhost -p 5432 -U your_db_user -d youtube
Check FFmpeg: ffmpeg -version

Project Structure
youtube-downloader/
├── app/
│   ├── config/                 # Configuration files
│   │   ├── celery.py           # Celery configuration
│   │   ├── settings.py         # Application settings
│   ├── db/                     # Database-related files
│   │   ├── init_db.py          # Deprecated (replaced by Alembic)
│   │   ├── session.py          # Async/sync database sessions
│   │   ├── alembic.ini         # Alembic configuration
│   │   ├── env.py             # Alembic environment
│   │   ├── script.py.mako      # Alembic migration template
│   │   ├── versions/           # Alembic migration scripts
│   ├── routers/
│   │   ├── download/
│   │   │   ├── endpoint.py     # FastAPI download endpoint
│   │   │   ├── models.py       # SQLAlchemy Video model
│   │   │   ├── repository.py   # Database interactions
│   │   │   ├── services.py     # Business logic
│   ├── services/
│   │   ├── s3.py              # S3 upload logic
│   ├── tasks/
│   │   ├── download.py        # Celery download task
│   ├── utils/
│   │   ├── ffmpeg_utils.py     # FFmpeg utility (checks availability)
│   │   ├── helpers.py         # General utilities
│   │   ├── storage.py         # Storage-related utilities
│   ├── main.py                # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── README.md                  # Project documentation

Running the Application

Start Redis:
redis-server


Start PostgreSQL:
sudo service postgresql start


Start FastAPI Server:
uvicorn app.main:app --reload


Start Celery Worker:
celery -A app.config.celery.celery_app worker --loglevel=info


Verify API:Open http://localhost:8000/docs in a browser to access the Swagger UI.


API Usage
Endpoint: Start Video Download

Method: POST
URL: /download
Body:{
  "video_id": "nYqBGORYWDU",
  "format": "mp4",
  "quality": "720p"
}


Response (Success):{
  "status": "download_started",
  "task_id": "<celery_task_id>"
}


Response (Failure):{
  "status": "failed",
  "reason": "Invalid format: xyz. Allowed formats: mp4, webm, mkv, mp3"
}



Example Request
curl -X POST http://localhost:8000/download \
-H "Content-Type: application/json" \
-d '{"video_id": "nYqBGORYWDU", "format": "mp4", "quality": "720p"}'

Notes

Formats: mp4, webm, mkv, mp3
Qualities: 360p, 480p, 720p, 1080p, 4k
MP3 Conversion: Requires FFmpeg.
Fallback: If yt-dlp fails, pytube is attempted twice before returning a failure.

Database Migrations
To create a new migration (e.g., after modifying app/routers/download/models.py):
alembic revision -m "description_of_change"

Edit the generated script in app/db/versions/ and apply:
alembic upgrade head

Troubleshooting

Celery Worker Fails:
Ensure Redis is running: redis-cli ping
Verify Celery module path: celery -A app.config.celery.celery_app worker --loglevel=info


Database Connection Errors:
Check .env variables (DB_HOST, DB_USER, etc.).
Verify PostgreSQL: psql -h localhost -p 5432 -U your_db_user -d youtube


FFmpeg Not Found:
Install FFmpeg: sudo apt-get install ffmpeg
Check path: ffmpeg -version


Download Failures:
Check Celery logs for yt-dlp or pytube errors.
Ensure video is available and not region-restricted.


Alembic Errors:
Verify alembic.ini and env.py configurations.
Run alembic upgrade head to apply migrations.



FAQs

Why use yt-dlp and pytube?yt-dlp is the primary downloader due to its robustness. pytube is a fallback for reliability.
Can I use a real S3 bucket?Yes, replace upload_to_mock_s3 in app/services/s3.py with real S3 upload logic using boto3.
How to scale the application?Deploy with Docker, use a production WSGI server (e.g., Gunicorn), and scale Celery workers.

Contributing

Fork the repository.
Create a feature branch: git checkout -b feature-name
Commit changes: git commit -m "Add feature"
Push to branch: git push origin feature-name
Open a pull request.

License
MIT License. See LICENSE for details.
