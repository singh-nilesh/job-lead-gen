from .base import router
from fastapi import HTTPException
from app.core.logger import api_logger as logger
from app.core.utils import generate_file_id
from app.tasks import generate_cover_letter
from app.tasks.interface import AsyncTaskResult


@router.get("/generate_cover_letter", response_model=AsyncTaskResult)
async def generate_cover_letter(
    user_id:str,
    job_data:str,
    personalization_input:str = "",
    ):
    ''' Endpoint to generate a cover letter based on user data and job description '''
    logger.info(f"generate_cover_letter called for user_id={user_id}")

    file_id = generate_file_id()
    try:
        task = generate_cover_letter.delay(
            file_id = file_id,
            job_data = job_data,
            personalization_input = personalization_input
        )
        return AsyncTaskResult(
            task_id= task.id,
            state= task.status,
            message= "Cover letter generation has been scheduled. use task id to check status"
        )
    
    except Exception as e:
        logger.error(f"Error scheduling cover letter generation for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error scheduling cover letter generation")