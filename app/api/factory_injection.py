""" factory Dependency injection generator"""

from fastapi import Depends
from functools import lru_cache

from app.db.mongo.motorConfig import get_app_db
from app.db.vector_store import get_vector_store


from app.services.cover_letter import CoverLetterService
from app.services.resume import ResumeIngestionService
from app.services.resume.generation_service import ResumeGenerationService


@lru_cache()
def get_resume_ingestion_service(
    db=Depends(get_app_db), 
    vector_store=Depends(get_vector_store)
    ) -> ResumeIngestionService:

    """ Dependency injector for ResumeIngestionService """
    return ResumeIngestionService(db=db, vector_store=vector_store)


@lru_cache()
def get_resume_generation_service(
    db=Depends(get_app_db), 
    vector_store=Depends(get_vector_store)
    ) -> 'ResumeGenerationService':

    """ Dependency injector for ResumeGenerationService """
    return ResumeGenerationService(db=db, vector_store=vector_store)


@lru_cache()
def get_cover_letter_service(
    db=Depends(get_app_db), 
    vector_store=Depends(get_vector_store)
    ) -> 'CoverLetterService':

    """ Dependency injector for CoverLetterService """
    from app.services.cover_letter import CoverLetterService
    return CoverLetterService(db=db, vector_store=vector_store)