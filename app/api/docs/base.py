from fastapi import APIRouter
from app.core.celery_config import celery_app
from app.tasks.interface import AsyncTaskResult

# docs router
router = APIRouter()


@router.get("/task/{task_id}", response_model=AsyncTaskResult)
async def get_task_status(task_id: str):
    """ 
    Endpoint to get the status and result of a Scheduled tasks 
    """
    task = celery_app.AsyncResult(task_id)
    
    response = AsyncTaskResult(
        task_id=task.id,
        state=task.state,
    )

    if task.state == "SUCCESS":
        meta = task.info or {}
        response['message'] = meta.get("message", "Task completed successfully")
        response['result'] = meta.get("result", None)
    
    elif task.state == "FAILURE":
        meta = task.info or {}
        response['message'] = meta.get("message", "Task failed")
        response['error'] = meta.get("error", None)
    
    else:
        response['message'] = "Task is still in progress"

    return response