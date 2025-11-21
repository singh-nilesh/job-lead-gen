from motor.motor_asyncio import AsyncIOMotorClient
from app.core.logger import service_logger as logger
from langchain_qdrant import QdrantVectorStore

from app.core.utils import set_user_id_all
from .helpers import _insert_resume_sections



class ResumeService:
    ''' Service to handle Operation related to Resume'''
    def __init__(self, db:AsyncIOMotorClient, VectorStore:QdrantVectorStore):
        self.db = db
        self.vector_store = VectorStore
    
    def get_resume_collection(self):
        pass

    async def _save_resume(self, resume: dict, user_id: int) -> bool:
        ''' Save resume to the App database (NOSQL) '''
        logger.info(f"Saving resume for user_id: {user_id}")

        # Ensure user_id is set in all sections
        set_user_id_all(resume, user_id)
        logger.debug(f"User_ID after setting user_id: {resume.profile.get('user_id')}")

        res = await _insert_resume_sections(self.db, resume)
        if res:
            logger.info(f"Successfully saved resume for user_id: {user_id}")
            return True
        else:
            logger.error(f"Failed to save resume for user_id: {user_id}")
            return False


    