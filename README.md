# 🎬 YouTube Video Downloader (YT Downloader Pro)

A **production-grade FastAPI** application for downloading YouTube videos asynchronously using **Celery**, storing metadata in **PostgreSQL**, and uploading videos to **S3** (mocked with Moto). The application supports audio/video format selection, multiple quality options, and robust error handling with retry mechanisms using `pytube` as a fallback to `yt-dlp`.

---

## 🚀 Features

- **Asynchronous Downloads**: Uses Celery with Redis for background processing.
- **Format & Quality Options**: Supports `mp4`, `webm`, `mkv`, and `mp3` formats. Quality options include `360p`, `480p`, `720p`, `1080p`, and `4k`.
- **Fallback Mechanism**: If `yt-dlp` fails, retries up to 2 times using `pytube`.
- **PostgreSQL Integration**: Stores video metadata using SQLAlchemy.
- **Mock S3 Uploads**: Uploads completed downloads to a mock S3 bucket using `boto3` and `moto`.
- **Database Migrations**: Alembic-based migration support.
- **Modular Design**: Organized codebase following separation of concerns and clean architecture.

---

## 🧰 Tech Stack

| Category     | Technologies Used                        |
|--------------|-------------------------------------------|
| **Framework** | FastAPI                                  |
| **Language**  | Python 3.12                              |
| **Database**  | PostgreSQL, SQLAlchemy (async + sync)   |
| **Task Queue**| Celery with Redis                        |
| **Downloader**| yt-dlp (primary), pytube (fallback)     |
| **Storage**   | boto3 with Moto for mock S3             |
| **Migrations**| Alembic                                 |
| **Other**     | FFmpeg for MP3 conversion               |

---

## ✅ Prerequisites

- Python 3.12+
- Redis
- PostgreSQL
- FFmpeg (for MP3 conversions)
- Virtual environment (recommended)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/youtube-downloader.git
cd youtube-downloader
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv yt
source yt/bin/activate  # Windows: yt\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies

#### Redis (Ubuntu):
```bash
sudo apt-get install redis-server
redis-server
```

#### PostgreSQL (Ubuntu):
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

#### FFmpeg:
```bash
sudo apt-get install ffmpeg
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
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
```

Load the variables:
```bash
export $(cat .env | xargs)
```

### 6. Set Up PostgreSQL Database

```bash
sudo -u postgres psql
CREATE DATABASE youtube;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE youtube TO your_db_user;
\q
```

### 7. Apply Database Migrations

```bash
alembic upgrade head
```

---

## 🧪 Verify Setup

- **Redis**: `redis-cli ping` (should return `PONG`)
- **PostgreSQL**: `psql -h localhost -p 5432 -U your_db_user -d youtube`
- **FFmpeg**: `ffmpeg -version`

---

## 📁 Project Structure

```
youtube-downloader/
├── app/
│   ├── config/
│   │   ├── celery.py
│   │   └── settings.py
│   ├── db/
│   │   ├── session.py
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── routers/
│   │   └── download/
│   │       ├── endpoint.py
│   │       ├── models.py
│   │       ├── repository.py
│   │       └── services.py
│   ├── services/
│   │   └── s3.py
│   ├── tasks/
│   │   └── download.py
│   ├── utils/
│   │   ├── ffmpeg_utils.py
│   │   ├── helpers.py
│   │   └── storage.py
│   └── main.py
├── .env
├── README.md
├── requirements.txt
```

---

## 🚀 Running the Application

### Start Redis
```bash
redis-server
```

### Start PostgreSQL
```bash
sudo service postgresql start
```

### Start FastAPI Server
```bash
uvicorn app.main:app --reload
```

### Start Celery Worker
```bash
celery -A app.config.celery.celery_app worker --loglevel=info
```

### Access API Docs
Open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Usage

### Endpoint: Start Video Download

- **Method**: `POST`
- **URL**: `/download`
- **Request Body**:
```json
{
  "video_id": "nYqBGORYWDU",
  "format": "mp4",
  "quality": "720p"
}
```

- **Success Response**:
```json
{
  "status": "download_started",
  "task_id": "<celery_task_id>"
}
```

- **Failure Response**:
```json
{
  "status": "failed",
  "reason": "Invalid format: xyz. Allowed formats: mp4, webm, mkv, mp3"
}
```

### Example Curl Request

```bash
curl -X POST http://localhost:8000/download \
-H "Content-Type: application/json" \
-d '{"video_id": "nYqBGORYWDU", "format": "mp4", "quality": "720p"}'
```

---

## 🛠 Database Migrations

Create a new migration:

```bash
alembic revision -m "add_new_column"
```

Apply it:

```bash
alembic upgrade head
```

---

## 🧯 Troubleshooting

### Celery Worker Issues
- Ensure Redis is running: `redis-cli ping`
- Verify Celery command: `celery -A app.config.celery.celery_app worker --loglevel=info`

### PostgreSQL Connection Errors
- Check your `.env` values
- Try: `psql -h localhost -p 5432 -U your_db_user -d youtube`

### FFmpeg Not Found
- Install using: `sudo apt-get install ffmpeg`
- Test with: `ffmpeg -version`

### Download Failures
- Check Celery logs
- Validate video accessibility and regional availability

---

## ❓ FAQs

**Q: Why use yt-dlp and pytube together?**  
A: `yt-dlp` is powerful but may fail in edge cases; `pytube` provides a reliable fallback.

**Q: Can I switch to real AWS S3?**  
A: Yes. Replace the mock upload logic in `app/services/s3.py` with actual `boto3` logic.

**Q: How do I scale this application?**  
A: Use Docker, Gunicorn for FastAPI, and scale out Celery workers.

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch: `git checkout -b feature-name`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Open a pull request

---

## 📄 License

**MIT License**  
See [LICENSE](./LICENSE) for details.
