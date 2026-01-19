""" Service Helper Functions """

from app.core.logger import service_logger as logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError


async def _insert_resume_sections(db: AsyncIOMotorDatabase, data: dict):
    ''' 
    Insert multiple resume sections into their respective collections (main_db)
    Auto-detects:
        - dict sections (profile)
        - list sections (education, work_experience)
    Returns:
        - dict of inserted IDs on success
        - False on failure
    '''
    doc_ids = {}
    try:
        logger.info("Inserting resume sections into collections")
        for key, value in data.items():
            collection = db[key]

            if isinstance(value, dict):
                # Single document (profile)
                result = await collection.insert_one(value)
                doc_ids[key] = {
                    "_id": result.inserted_id,
                    "data": value
                }
                logger.info(f"Inserted profile section into collection: {key}")

            elif isinstance(value, list):
                # Multiple documents (education, work_experience)
                if value:
                    results = await collection.insert_many(value)
                    doc_ids[key] = {
                        "_ids": results.inserted_ids,
                        "data": value
                    }
                    logger.info(f"Inserted {len(value)} items into collection: {key}")

        logger.info("Finished inserting resume sections successfully")
        return doc_ids

    except PyMongoError as pe:
        logger.error(f"PyMongo error while inserting resume sections - {str(pe)}")
        return False
    except Exception as e:
        logger.error(f"Error inserting resume sections - {str(e)}")
        return False


async def _get_user_data(db_ids:dict, user_id:str, db: AsyncIOMotorDatabase):
    ''' Retrieve complete user data from main DB based on provided IDs.
    args:
        db_ids: {section: list of ObjectId}
        user_id: str, 
        db: main_db client
    returns:
        dict: Complete user data from main DB - {section: list of data dict}
    '''
    logger.info("Quering complete user data from main database.")
    result = {}

    # Query User profile data
    profile = await db.profile.find_one(
        {"user_id": user_id},
        {"_id": 0, "user_id": 0}  # exclude user_id and _id fields
    )
    if profile:
        result["profile"] = profile
    else:
        logger.warning(f"No profile data found for user_id:{user_id}")
    
    # Query other sections from main db
    for section, ids in db_ids.items():
        cursor = db[section].find(
            {"_id": {"$in": ids}},
            {"user_id": 0, "_id": 0}
        )
        docs = await cursor.to_list(length=None)
        if not docs:
            logger.warning(f"No data found in section:{section} for ids:{ids}")
            continue
        result[section] = docs
    
    logger.info("User data queried successfully from main database.")
    return result


