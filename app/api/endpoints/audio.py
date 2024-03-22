from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List
from app.schemas import Audio, AudioCreate, AudioUpdate
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from app.models.audio import Audio as DBAudio
from fastapi import Form, File, UploadFile


import os

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/audios/", response_model=List[Audio])
def read_audios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    audios = db.query(DBAudio).offset(skip).limit(limit).all()
    return audios


@router.post("/audios/", response_model=Audio)
def create_audio(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    duration: float = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    audio_file: UploadFile = File(...),
    cover_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Define the upload directory
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Save audio file
    audio_path = os.path.join(upload_dir, audio_file.filename)
    with open(audio_path, "wb") as buffer:
        buffer.write(audio_file.file.read())

    # Save cover file
    cover_path = os.path.join(upload_dir, cover_file.filename)
    with open(cover_path, "wb") as buffer:
        buffer.write(cover_file.file.read())

    db_audio = DBAudio(
        title=title,
        artist=artist,
        album=album,
        duration=duration,
        file_path=audio_path,
        cover_path=cover_path,
        genre=genre,
        year=year,
    )
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


@router.put("/audios/{audio_id}", response_model=Audio)
def update_audio(
    audio_id: int,
    audio: AudioUpdate,
    audio_file: UploadFile = File(None),
    cover_file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    db_audio = db.query(DBAudio).filter(DBAudio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")

    update_data = audio.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_audio, key, value)

    # Update audio file if provided
    if audio_file:
        audio_path = f"uploaded_files/audios/{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            buffer.write(audio_file.file.read())
        db_audio.file_path = audio_path

    # Update cover file if provided
    if cover_file:
        cover_path = f"uploaded_files/covers/{cover_file.filename}"
        with open(cover_path, "wb") as buffer:
            buffer.write(cover_file.file.read())
        db_audio.cover_path = cover_path

    db.commit()
    db.refresh(db_audio)
    return db_audio
