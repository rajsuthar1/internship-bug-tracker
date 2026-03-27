from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.db.session import engine
from app.models.base import Base
# Import models here to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.project import Project
from app.models.issue import Issue

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if any) goes here

app = FastAPI(
    title="Bug Tracker API",
    description="A high-performance Issue Tracking System inspired by Jira and Linear.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Bug Tracker API is live", "status": "healthy"}

app.include_router(api_router, prefix="/api/v1")