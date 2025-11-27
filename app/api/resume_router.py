from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import tempfile

from app.core.logger import api_logger as logger
from app.services.resume import ResumeIngestionService
from .factory_injection import get_resume_ingestion_service




router = APIRouter()

@router.get("/generate")
def get_resume(Job_context:str, resume_id: int):
    """ Retrieve resume by ID """
    # Log request
    logger.info(f"get_resume called with Job_context={Job_context!r}, resume_id={resume_id}")
    # Placeholder implementation
    return {"resume_id": resume_id, "content": "Resume content goes here"}


@router.post("/upload")
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