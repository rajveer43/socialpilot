from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "social_reply_generator"

# Async client for FastAPI endpoints
async_client = AsyncIOMotorClient(MONGODB_URI)
async_db = async_client[DATABASE_NAME]

# Sync client for background tasks
sync_client = MongoClient(MONGODB_URI)
sync_db = sync_client[DATABASE_NAME]

# Collection for storing replies
replies_collection = async_db.replies

async def store_reply(platform: str, post_text: str, generated_reply: str, timestamp: str):
    """Store a generated reply in the database."""
    reply_doc = {
        "platform": platform,
        "post_text": post_text,
        "generated_reply": generated_reply,
        "timestamp": timestamp
    }
    await replies_collection.insert_one(reply_doc)
    return reply_doc 