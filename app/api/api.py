from fastapi import APIRouter
from .endpoints import audio

router = APIRouter()

router.include_router(audio.router, prefix="/audio")
