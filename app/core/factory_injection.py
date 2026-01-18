""" factory Dependency injection generator"""

from functools import lru_cache

from app.db.mongo.motorConfig import get_app_db
from app.db.vector_store import get_vector_store

from app.services.cover_letter import CoverLetterService
from app.services.resume import ResumeIngestionService, ResumeGenerationService


@lru_cache()
def get_worker_deps():
    db = get_app_db()
    vector_store = get_vector_store()
    return db, vector_store


def get_resume_ingestion_service() -> ResumeIngestionService:
    """ Dependency injector for ResumeIngestionService """
    db, vector_store = get_worker_deps()
    return ResumeIngestionService(db=db, vector_store=vector_store)
    

def get_resume_generation_service() -> 'ResumeGenerationService':
    """ Dependency injector for ResumeGenerationService """
    db, vector_store = get_worker_deps()
    return ResumeGenerationService(db=db, vector_store=vector_store)


def get_cover_letter_service() -> CoverLetterService:
    """ Dependency injector for CoverLetterService """
    db, vector_store = get_worker_deps()
    return CoverLetterService(db=db, vector_store=vector_store)