# 🚀 YT Downloader Pro

A **production-grade FastAPI** application for downloading YouTube videos and audio asynchronously using **Celery**, storing metadata in **PostgreSQL**, and uploading downloaded files to **S3** (mock implementation via Moto). The application includes a fallback to **pytube** when **yt-dlp** fails and supports multiple video/audio formats and quality options.

---

## 📌 Features

- **Asynchronous Downloads**: Uses Celery with Redis for non-blocking background video downloads.
- **Format & Quality Options**: Supports `mp4`, `webm`, `mkv`, and `mp3` with qualities like `360p`, `480p`, `720p`, `1080p`, and `4k`.
- **Fallback Mechanism**: If `yt-dlp` fails, retries download using `pytube` (up to 2 attempts).
- **Metadata Storage**: Stores video metadata in PostgreSQL using async SQLAlchemy.
- **S3 Integration**: Uploads files to a mock S3 bucket using `boto3` and `moto`.
- **Database Migrations**: Schema managed using Alembic.
- **Production-Grade Architecture**: Modular and scalable codebase, following clean architecture principles.

---

## 🛠 Tech Stack

| Component       | Technology                          |
|----------------|--------------------------------------|
| **Backend**     | FastAPI, Python 3.12                 |
| **Task Queue**  | Celery with Redis                   |
| **Database**    | PostgreSQL, SQLAlchemy (async/sync) |
| **Downloader**  | yt-dlp (primary), pytube (fallback) |
| **Storage**     | Mock S3 (via moto + boto3)          |
| **Migrations**  | Alembic                             |
| **Dependencies**| Managed via `requirements.txt`      |

... (truncated for brevity — full content will be included in the file)

---

## 📄 License

**MIT License**  
See the [LICENSE](./LICENSE) file for details.
