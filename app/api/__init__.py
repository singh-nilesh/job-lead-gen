"""API package for routers"""

from .auth_router import router as auth
from .docs.base import router as docs_base


__all__ = ["auth", "docs_base"]

def include_routers(app):
    """Include all routers in the FastAPI app"""
    app.include_router(auth, prefix="/auth", tags=["auth"])
    app.include_router(docs_base, prefix="/docs", tags=["documents"])