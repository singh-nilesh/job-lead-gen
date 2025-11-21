''' 
Configuration file for motor Client
- Database: MongoDB
- Usage: App data (main database)
'''

from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache
from app.core.config import Settings
from typing import AsyncGenerator
from app.db.mongo import schema



NOSQL_DATABASE_URL = Settings.MONGO_URL  # Full URL with DB
print("MONGO URL",NOSQL_DATABASE_URL)

@lru_cache()
def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(NOSQL_DATABASE_URL)


# Dependency to get App database
async def get_app_db() -> AsyncGenerator:
    """ Dependency to get MongoDB database """
    client = get_mongo_client()
    db = client.get_default_database()  # DB from url
    try:
        yield db
    finally:
        pass  # Motor handles cleanup internally


# Initialization function for app startup
async def init_nosql_db():
    """ Initialize collections - for app startup """
    global client
    if client is None:
        client = AsyncIOMotorClient(NOSQL_DATABASE_URL)
        print("[*] Created MongoDB client connection, for collection initialization")
    
    db = client.get_default_database()
    print(f"[*] Initializing MongoDB database: {db.name}")

    collection_list = schema.__all__
    print(f"[*] Required collections to ensure: {collection_list}")
    existing_collections = await db.list_collection_names()
    print(f"[*] Found {len(existing_collections)} existing collections: {existing_collections}")
    
    # Create collections if not present
    for coll_name in collection_list:
        if coll_name not in existing_collections:
            try:
                await db.create_collection(coll_name)
                await db[coll_name].create_index("profile_id")
                print(f"[*] Created collection: {coll_name}")
                
                # Each profile has a unique email
                if coll_name == "profile":
                    await db[coll_name].create_index("email", unique=True)
                    print(f"[*] Created unique email index for: {coll_name}")
               
            except Exception as e:
                print(f"[x] Error creating collection {coll_name}: {e}")
        else:
            print(f"[*] Collection {coll_name} already exists")
    
    new_collections = await db.list_collection_names()
    print(f"[*] Total collections after initialization: {len(new_collections)} - {new_collections}")
    print("[*] Database initialization completed")



# Cleanup function for tests
async def teardown_nosql_db():
    """ Drop all collections - for test cleanup """
    global client
    if client is not None:
        db = client.get_default_database()
        collection_names = await db.list_collection_names()        
        for name in collection_names:
            try:
                await db.drop_collection(name)
                print(f"Dropped collection: {name}")
            except Exception as e:
                print(f"Error dropping collection {name}: {e}")
    else:
        print("No MongoDB client to teardown")

