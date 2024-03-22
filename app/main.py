from fastapi import FastAPI
from .api.api import router as api_router
from .database.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api")
