"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI

from src.api.routes import router as rag_router
from src.api.auth import router as auth_router
from src.db.mongo_client import init_db

app = FastAPI(title="Adaptive RAG API")
app.include_router(auth_router)
app.include_router(rag_router)
app.state.description_ = ""

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"message": "Adaptive RAG API is running"}
