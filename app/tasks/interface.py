""" Return types for celery tasks """

from pydantic import BaseModel
from typing import Optional, Literal, Dict, Any

class AsyncTaskResult(BaseModel):
    task_id: str
    state: Literal["PENDING", "STARTED", "SUCCESS", "FAILURE"]
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None



def failure_meta(message: str, error: Optional[str] = None):
        return {
              "message": message,
              "error": error
        }

def success_meta(message: str, result: Optional[Any] = None):
        return {
              "message": message,
              "result": result
        }

def file_payload(file_id: str, download_url: str):
    return {
        "file_id": file_id,
        "download_url": download_url
    }
