""" Resume Service Helper Functions """

from app.core.logger import service_logger as logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

async def _insert_resume_sections(db:AsyncIOMotorClient, data: dict):
        ''' 
        Insert multiple resume sections into their respective collections 
        Auto-detects:
            - dict sections (profile)
            - list sections (education, work_experience)
        '''
        try:
            logger.info("Inserting resume sections into collections")
            for key, value in data.items():
                collection = db[key]

                if isinstance(value, dict):
                    # Single document (profile)
                    await collection.insert_one(value)
                    logger.info(f"Inserted profile section into collection: {key}")

                elif isinstance(value, list):
                    # Multiple documents (education, work_experience)
                    if value:
                        await collection.insert_many(value)
                        logger.info(f"Inserted {len(value)} items into collection: {key}")

            logger.info("Finished inserting resume sections successfully")
            return True
        except PyMongoError as pe:
            logger.error(f"PyMongo error while inserting resume sections - {str(pe)}")
            return False
        except Exception as e:
            logger.error(f"Error inserting resume sections - {str(e)}")
            return False
