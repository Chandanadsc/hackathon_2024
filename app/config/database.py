from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "plagiarism_detector"

# Async client for main operations
async def get_async_db():
    client = AsyncIOMotorClient(MONGODB_URI)
    return client[DB_NAME]

# Sync client for vector operations
def get_sync_db():
    client = MongoClient(MONGODB_URI)
    return client[DB_NAME]

# Create indexes
def setup_indexes():
    db = get_sync_db()
    
    # Create vector search index for documents
    db.documents.create_index([
        ("content_vector", "vectorSearch")
    ], {
        "vectorSearchOptions": {
            "numDimensions": 768,  # For BERT embeddings
            "similarity": "cosine"
        }
    })

    # Create regular indexes
    db.users.create_index("email", unique=True)
    db.documents.create_index("user_id")
    db.reports.create_index("user_id")
    db.reports.create_index("document_id")
    db.cache.create_index("created_at", expireAfterSeconds=86400)  # 24 hour cache

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed)