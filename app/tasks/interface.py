""" Return types for celery tasks """

from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any


class AsyncTaskResult(BaseModel):
    task_id: str
    state: Literal["PENDING", "STARTED", "SUCCESS", "FAILURE"]
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


""" Helper functions to create standardized meta information 
    for Celery task results,

    dataclasses cannot be used directly in Celery task meta,
    hence using simple dicts.
"""


def failure_meta(message: str, error: Optional[str] = None) -> dict:
    return {
        "message": message,
        "error": error,
    }


def success_meta(message: str, result: Optional[Any] = None) -> dict:
    return {
        "message": message,
        "result": result,
    }


def file_payload(file_id: str, download_url: str) -> dict:
    return {
        "file_id": file_id,
        "download_url": download_url,
    }