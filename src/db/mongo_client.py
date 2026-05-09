"""
MongoDB client initialization.
"""

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings

# If MONGODB_URL is not set in settings, we can fallback or use a default
import os
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "adaptive_rag")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db["users"]

async def init_db():
    """Initialize database indexes."""
    # Ensure email is unique in users collection
    await users_collection.create_index("email", unique=True)
