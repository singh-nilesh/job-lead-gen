"""API package for routers"""

from .auth_router import router as auth


__all__ = ["auth"]


def include_routers(app):
    """Include all routers in the FastAPI app"""
    app.include_router(auth, prefix="/auth", tags=["auth"])
    