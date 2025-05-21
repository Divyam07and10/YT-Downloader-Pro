from fastapi import APIRouter, HTTPException
from app.routers.download.schemas import DownloadRequest

router = APIRouter()

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']

@router.post("")
async def download_video_endpoint(request: DownloadRequest):
    from app.routers.download.services import download_video_handler
    # Explicitly validate format and quality
    if request.format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "failed",
                "reason": f"Invalid format: {request.format}. Allowed formats: {', '.join(ALLOWED_FORMATS)}"
            }
        )
    if request.quality not in ALLOWED_QUALITIES:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "failed",
                "reason": f"Invalid quality: {request.quality}. Allowed qualities: {', '.join(ALLOWED_QUALITIES)}"
            }
        )
    return await download_video_handler(request.video_id, request.format, request.quality)