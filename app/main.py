import os
import glob
import shutil
import asyncio
from fastapi import FastAPI
from app.routers.download.endpoint import router as download_router

app = FastAPI(title="YouTube Video Downloader")

@app.on_event("startup")
async def startup():
    """Clear /tmp/videos directory on server startup."""
    tmp_videos_path = '/tmp/videos'
    try:
        if os.path.exists(tmp_videos_path):
            for item in glob.glob(os.path.join(tmp_videos_path, '*')):
                try:
                    if os.path.isfile(item):
                        await asyncio.to_thread(os.remove, item)
                    elif os.path.isdir(item):
                        await asyncio.to_thread(shutil.rmtree, item)
                except:
                    pass
            if not os.listdir(tmp_videos_path):
                await asyncio.to_thread(os.rmdir, tmp_videos_path)
    except:
        pass

app.include_router(download_router, prefix="/download")