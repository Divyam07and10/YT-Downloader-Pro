import re
import yt_dlp
import shutil
from fastapi import HTTPException
from app.config.celery import celery_app
from app.tasks.download import download_video_task
from app.utils.storage import check_file_size, check_storage_limit
from app.utils.ffmpeg_checker import check_ffmpeg
from app.utils.helpers import build_format_selector
from app.config.settings import MAX_VIDEO_SIZE

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']

def sanitize_video_id(video_id: str) -> str:
    """Sanitize and validate YouTube video ID."""
    if not re.match(r'^[A-Za-z0-9_-]{11}$', video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube video ID")
    sanitized_id = re.sub(r'[^A-Za-z0-9_-]', '', video_id)
    if len(sanitized_id) != 11:
        raise HTTPException(status_code=400, detail="Invalid YouTube video ID length")
    return sanitized_id

def check_storage_and_size(estimated_size: int = 0):
    """Check if estimated size exceeds 100MB limit."""
    if estimated_size > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail=f"Estimated video size ({estimated_size / 1024 / 1024:.2f} MB) exceeds 100 MB limit")
    return True

def get_estimated_size(youtube_url: str, format: str, quality: str, ffmpeg_available: bool) -> int:
    """Estimate video file size using yt-dlp."""
    try:
        target_height = 2160 if quality.lower() == "4k" else int(quality.lower().replace("p", ""))
        format_str = build_format_selector(format, target_height)
        ydl_opts = {
            "format": format_str,
            "simulate": True,
            "socket_timeout": 30,
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_size = info.get("filesize_approx", 0) or info.get("filesize", 0)
            return video_size if video_size else 0
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to estimate video size: {str(e)}")

async def download_video_handler(video_id: str, format: str, quality: str):
    """Dispatch video download task to Celery in the background."""
    try:
        # Validate format and quality
        if format not in ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "failed",
                    "reason": f"Invalid format: {format}. Allowed formats: {', '.join(ALLOWED_FORMATS)}"
                }
            )
        if quality not in ALLOWED_QUALITIES:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "failed",
                    "reason": f"Invalid quality: {quality}. Allowed qualities: {', '.join(ALLOWED_QUALITIES)}"
                }
            )

        # Validate video ID
        sanitized_id = sanitize_video_id(video_id)
        youtube_url = f"https://www.youtube.com/watch?v={sanitized_id}"
        
        # Validate FFmpeg for MP3 format
        ffmpeg_path = shutil.which("ffmpeg") or "/opt/bin/ffmpeg"
        ffmpeg_available = check_ffmpeg(ffmpeg_path)
        if format == "mp3" and not ffmpeg_available:
            raise HTTPException(status_code=400, detail=f"MP3 format requires ffmpeg, which is not available at {ffmpeg_path}")

        # Estimate size and validate
        estimated_size = get_estimated_size(youtube_url, format, quality, ffmpeg_available)
        check_storage_and_size(estimated_size=estimated_size)
        
        # Check /tmp storage limit
        check_storage_limit()
        
        # Dispatch Celery task in the background
        task = download_video_task.delay(youtube_url, format, quality)
        
        return {
            "status": "download_started",
            "task_id": task.id
        }
    except Exception as e:
        print(f"[debug] General Exception: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "failed",
                "reason": f"Task dispatch failed: {str(e)}"
            }
        )