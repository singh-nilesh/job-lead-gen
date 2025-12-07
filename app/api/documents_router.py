import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import tempfile

from app.core.logger import api_logger as logger
from app.core.exception import ServiceException
from app.services.resume import ResumeIngestionService, ResumeGenerationService
from app.services.cover_letter import CoverLetterService
from .factory_injection import get_resume_ingestion_service, get_resume_generation_service, get_cover_letter_service




router = APIRouter()

@router.get("/generate_resume")
async def generate_resume(
    user_id:str, 
    job_data:str,
    background_tasks: BackgroundTasks,
    service: ResumeGenerationService = Depends(get_resume_generation_service)
    ):
    ''' Endpoint to generate a resume based on user data and job description '''
    logger.info(f"generate_resume called for user_id={user_id}")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    output_path = temp_file.name
    temp_file.close()

    try:
        resume_path =  await service.generate(
            user_id=user_id, 
            job_data=job_data, 
            output_path=output_path
            )
        logger.info(f"Resume generated at {resume_path} for user_id={user_id}")
        
        # Sechudule file for deletion after response
        background_tasks.add_task(os.remove, resume_path)

        return FileResponse(
            path=resume_path,
            filename=f"resume_{user_id}.docx",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except ServiceException as se:
        raise se
    except Exception as e:
        logger.error(f"Error generating resume for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error generating resume")


@router.post("/upload_resume")
async def upload_resume(
    user_id: str,
    file:UploadFile = File(..., description="Upload resume file (PDF or DOCX)"), 
    service: ResumeIngestionService = Depends(get_resume_ingestion_service)
    ):
    """ Endpoint to Ingest resume file into the system """
    logger.info(f"upload_resume called for user_id={user_id}, filename={file.filename}")

    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx')):
        logger.warning(f"Invalid file type for user_id={user_id}, filename={file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are allowed.")
    
    ext = ".pdf" if file.filename.endswith(".pdf") else ".docx"
    # Store the file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=ext) as temp_file:
            temp_file.write(await file.read())
            logger.debug(f"Written temp file at {temp_file.name} for user_id={user_id}")
            res = await service.ingest(temp_file.name, user_id)
            if not res:
                logger.error(f"Ingestion failed for user_id={user_id}, temp_file={temp_file.name}")
                raise HTTPException(status_code=500, detail="Failed to ingest resume")
            logger.info(f"Successfully ingested resume for user_id={user_id}, file={file.filename}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error ingesting resume for user_id={user_id}, file={file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error ingesting resume")
           
    return {"resume": file.filename, "status": "Resume uploaded successfully"}


@router.get("/generate_cover_letter")
async def generate_cover_letter(
    user_id:str,
    job_data:str,
    background_tasks: BackgroundTasks,
    personalization_input:str = "",
    service: CoverLetterService = Depends(get_cover_letter_service)
    ):
    ''' Endpoint to generate a cover letter based on user data and job description '''
    logger.info(f"generate_cover_letter called for user_id={user_id}")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    output_path = temp_file.name
    temp_file.close()

    try:
        cover_letter_path =  await service.generate_from_text(
            user_id=user_id, 
            job_data=job_data, 
            file_path=output_path,
            user_personalized_input=personalization_input
            )
        logger.info(f"Cover letter generated at {cover_letter_path} for user_id={user_id}")
        
        # Sechudule file for deletion after response
        background_tasks.add_task(os.remove, cover_letter_path)

        return FileResponse(
            path=cover_letter_path,
            filename=f"cover_letter_{user_id}.docx",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except ServiceException as se:
        raise se
    except Exception as e:
        logger.error(f"Error generating cover letter for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error generating cover letter")