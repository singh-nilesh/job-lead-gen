from fastapi import APIRouter
from app.core.celery_config import celery_app
from app.tasks.interface import AsyncTaskResult
from .coverletter_router import router as coverletter_router
from .resume_router import router as resume_router

# docs router
router = APIRouter()

# include sub-routers
router.include_router(resume_router)
router.include_router(coverletter_router)


# Unified endpoint to get task status
@router.get("/task_status/{task_id}", response_model=AsyncTaskResult)
async def get_task_status(task_id: str):

    task = celery_app.AsyncResult(task_id)
    meta = task.info if isinstance(task.info, dict) else {}

    if task.state == "SUCCESS":
        return AsyncTaskResult(
            task_id=task.id,
            state=task.state,
            message=meta.get("message", "Task completed successfully"),
            result=meta.get("result"),
        )

    if task.state == "FAILURE":
        return AsyncTaskResult(
            task_id=task.id,
            state=task.state,
            message=meta.get("message", "Task failed"),
            error=meta.get("error"),
        )

    return AsyncTaskResult(
        task_id=task.id,
        state=task.state,
        message="Task is still in progress",
    )
