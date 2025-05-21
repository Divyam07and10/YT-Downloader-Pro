from app.db.session import SessionLocal
from app.routers.download.models import Video

def insert_metadata(metadata: dict, s3_url: str, format: str) -> int:
    """Insert video metadata into the database synchronously."""
    with SessionLocal() as session:
        try:
            video = Video(
                url=metadata["url"],
                youtube_id=metadata["youtube_id"],
                title=metadata["title"],
                duration=metadata["duration"],
                views=metadata["views"],
                likes=metadata["likes"],
                channel=metadata["channel"],
                thumbnail_url=metadata["thumbnail_url"],
                resolution=metadata["resolution"],
                s3_url=s3_url,
                published_date=metadata["published_date"],
                format=format
            )
            session.add(video)
            session.commit()
            return video.id
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to insert metadata: {str(e)}")