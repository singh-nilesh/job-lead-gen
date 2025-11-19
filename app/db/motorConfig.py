''' 
Configuration file for motor Client
- Database: MongoDB
- Usage: App data (main database)
'''

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Settings
from typing import AsyncGenerator

NOSQL_DATABASE_URL = Settings.MONGO_URL
DB_NAME = Settings.MONGO_DB

client:AsyncIOMotorClient = None


# Dependency to get App database
async def get_app_db() -> AsyncGenerator:
    """ Dependency to get MongoDB database """
    global client
    if client is None:
        client = AsyncIOMotorClient(NOSQL_DATABASE_URL)
    db = client[DB_NAME]
    try:
        yield db
    finally:
        pass  # Motor handles cleanup internally


# Collection Initialization function
async def init_nosql_db():
    """ Initialize collections - for app startup """
    global client
    if client is None:
        client = AsyncIOMotorClient(NOSQL_DATABASE_URL)
    db = client[DB_NAME]

    collection_list = ["profile", "education", "work_exp", "projects"]
    existing_collections = await db.list_collection_names()

    # Create collections if not present
    for coll_name in collection_list:
        if coll_name not in existing_collections:
            await db.create_collection(coll_name)
            await db[coll_name].create_index("profile_id")

            # Unique for email in profile collection
            if coll_name == "profile":
                await db[coll_name].create_index("email", unique=True)
            

# Cleanup function for tests
async def teardown_nosql_db():
    """ Drop all collections - for test cleanup """
    global client
    if client is not None:
        db = client[DB_NAME]
        collection_names = await db.list_collection_names()
        for name in collection_names:
            await db.drop_collection(name)


