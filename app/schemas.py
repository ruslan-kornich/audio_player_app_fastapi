from pydantic import BaseModel
from typing import Optional


class AudioBase(BaseModel):
    title: Optional[str]
    artist: Optional[str]
    album: Optional[str]
    duration: Optional[float]
    genre: Optional[str]
    year: Optional[int]

    class Config:
        from_attributes = True


class AudioCreate(AudioBase):
    audio_file: str
    cover_file: str


class AudioUpdate(AudioBase):
    audio_file: Optional[str] = None
    cover_file: Optional[str] = None


class Audio(AudioBase):
    id: int

    class Config:
        from_attributes = True
