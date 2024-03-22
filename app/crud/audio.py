from sqlalchemy.orm import Session
from app.models.audio import Audio


def get_audios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Audio).offset(skip).limit(limit).all()


def create_audio(
    db: Session,
    title: str,
    artist: str,
    album: str,
    duration: float,
    file_path: str,
    cover_path: str,
    genre: str,
    year: int,
):
    db_audio = Audio(
        title=title,
        artist=artist,
        album=album,
        duration=duration,
        file_path=file_path,
        cover_path=cover_path,
        genre=genre,
        year=year,
    )
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


def get_audio(db: Session, audio_id: int):
    return db.query(Audio).filter(Audio.id == audio_id).first()


def delete_audio(db: Session, audio_id: int):
    db.query(Audio).filter(Audio.id == audio_id).delete()
    db.commit()
