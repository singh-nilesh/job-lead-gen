from fastapi import APIRouter, HTTPException, UploadFile, File
from app.tasks.interface import AsyncTaskResult

from app.core.logger import api_logger as logger
from app.db.s3_adapters import ObjectStorage
from app.tasks import ingest_resume, generate_resume
from app.core.utils import generate_file_id


router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

@router.get("/generate", response_model=AsyncTaskResult)
async def resume_generate(
    user_id:str, 
    job_data:str,
    ):
    ''' Endpoint to generate a resume based on user data and job description '''
    logger.info(f"generate_resume called for user_id={user_id}")

    file_id = generate_file_id(f"generated_resume_{user_id}.docx")
    try:
        task = generate_resume.delay(
            user_id = user_id,
            file_id = file_id,
            job_data = job_data
        )
        return AsyncTaskResult(
            task_id= task.id,
            state= task.status,
            message= "Resume generation has been scheduled. use task id to check status"
        )
    
    except Exception as e:
        logger.error(f"Error scheduling resume generation for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error scheduling resume generation")
    


@router.post("/upload", response_model=AsyncTaskResult)
async def resume_upload(
    user_id: str,
    file:UploadFile = File(..., description="Upload resume file (PDF or DOCX)"), 
    ):
    """ 
    Endpoint to Ingest resume file into the system 
    """
    logger.info(f"upload_resume called for user_id={user_id}, filename={file.filename}")

    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        logger.warning(f"Invalid file type for user_id={user_id}, filename={file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are allowed.")
    
    ext = ".pdf" if file.filename.endswith(".pdf") else ".docx"
    
    s3 = ObjectStorage()
    file_id = generate_file_id(file.filename)
    try:
        # Upload file to S3, and trigger ingestion task
        s3.upload_fileobj(file.file, file_id=file_id)

        task = ingest_resume.delay(
            user_id=user_id,
            file_id=file_id,
            file_ext=ext
            )

        return AsyncTaskResult(
            task_id= task.id,
            state= task.status,
            message= "Resume ingestion has been scheduled. use task id to check status"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error ingesting resume for user_id={user_id}, file={file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error ingesting resume")
           


