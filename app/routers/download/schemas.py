from pydantic import BaseModel, Field

ALLOWED_FORMATS = ['mp4', 'webm', 'mkv', 'mp3']
ALLOWED_QUALITIES = ['360p', '480p', '720p', '1080p', '4k']

class DownloadRequest(BaseModel):
    video_id: str
    format: str = Field(default='mp4', enum=ALLOWED_FORMATS)
    quality: str = Field(default='720p', enum=ALLOWED_QUALITIES)