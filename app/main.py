"""FastAPI application entry point"""
from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app.models import Base
from app.routes import authors, posts, comments

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A simple Blog API with FastAPI and SQLite",
    version="1.0.0"
)

# Include routers
app.include_router(authors.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
