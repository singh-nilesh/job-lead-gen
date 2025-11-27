"""API package for routers"""

from .auth_router import router as auth
from .resume_router import router as resume


__all__ = ["auth", "resume"]

def include_routers(app):
    """Include all routers in the FastAPI app"""
    app.include_router(auth, prefix="/auth", tags=["auth"])
    app.include_router(resume, prefix="/resume", tags=["resume"])