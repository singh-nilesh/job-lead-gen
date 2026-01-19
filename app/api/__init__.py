"""API package for routers"""

from .auth_router import router as auth
from .docs.router import router as docs


__all__ = ["auth", "docs"]

def include_routers(app):
    """Include all routers in the FastAPI app"""
    app.include_router(auth, prefix="/auth", tags=["auth"])
    app.include_router(docs, prefix="/docs")