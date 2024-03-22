from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, index=True)
    duration = Column(Float)
    file_path = Column(String, index=True)
    cover_path = Column(String, index=True)
    genre = Column(String, index=True)
    year = Column(Integer)
