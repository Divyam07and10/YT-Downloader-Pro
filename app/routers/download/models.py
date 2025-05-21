from sqlalchemy import Column, String, Integer, DateTime
from app.db.base import Base
from datetime import datetime

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    youtube_id = Column(String, nullable=False)
    title = Column(String)
    duration = Column(String)
    views = Column(Integer)
    likes = Column(Integer, nullable=True)
    channel = Column(String)
    thumbnail_url = Column(String)
    resolution = Column(String)
    s3_url = Column(String)
    published_date = Column(String)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    format = Column(String, nullable=False)