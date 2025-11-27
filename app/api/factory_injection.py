""" factory Dependency injection generator"""

from fastapi import Depends
from functools import lru_cache

from app.db.mongo.motorConfig import get_app_db
from app.db.vector_store import get_vector_store


from app.services.resume import ResumeIngestionService


@lru_cache()
def get_resume_ingestion_service(
    db=Depends(get_app_db), 
    vector_store=Depends(get_vector_store)
    ) -> ResumeIngestionService:

    """ Dependency injector for ResumeIngestionService """
    return ResumeIngestionService(db=db, vector_store=vector_store)
