import os
import tempfile
from app.core.exception import CustomException
from app.core.celery_config import celery_app
from app.core.factory_injection import get_resume_ingestion_service, get_resume_generation_service
from app.db.s3_adapters import ObjectStorage
from app.tasks.interface import file_payload, failure_meta, success_meta
from celery.exceptions import Ignore


# Celery task for ingesting resume file
@celery_app.task(bind=True)
def ingest_resume(self, file_id: str, file_ext:str = ".pdf") -> None:
    ''' Celery task for ingesting resume file '''
    
    s3_client = ObjectStorage()
    service = get_resume_ingestion_service()

    local_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            local_file_path = temp_file.name
        temp_file.close()

        # Download file from S3 to temp location
        if not s3_client.download(
            file_id=file_id,
            download_path=local_file_path
        ):
            self.update_state(
                state='FAILURE', 
                meta=failure_meta(
                    message=f" Failed to download resume from S3 for file_id:{file_id} ",
                    error="S3DownloadError"
            ))
            raise Ignore() # permanent failure, no retries
        
        # Ingest resume
        if not service.ingest(
            resume_filepath=local_file_path,
            user_id=f" CeleryTask-{self.request.id} "
        ):
            self.update_state(
                state='FAILURE',
                meta=failure_meta(
                    message=f" Resume ingestion failed for file_id:{file_id} ",
                    error="ResumeIngestionError"
            ))
            raise Ignore() # end task
        
        """ 
        pending improvement:
        [ ] Consider storing ingested file_id to user DB, for later reference and analytics.
        [ ] Can also be used to list uploaded resumes/docs for a user.
        """
        
        # success response
        payload = file_payload(
            file_id= file_id,
            download_url= s3_client.get_public_url(file_id)
        )
        self.update_state(
            state='SUCCESS', 
            meta= success_meta(
                message="Resume ingested successfully",
                result= payload
            ))
        return payload
    
    except Exception as e:
        raise CustomException(f"Unexpected error ingesting resume for file_id:{file_id}: {e}", status_code=500)
    
    finally:
        # file Cleanup
        os.remove(local_file_path) if local_file_path and os.path.exists(local_file_path) else None



# Celery task for generating resume
@celery_app.task(bind=True)
def generate_resume(self, job_data: str, file_id:str) -> None:
    ''' 
    Celery task for generating resume based on job data
    Args:
        job_data: The job description or data to tailor the resume.
        file_id: The S3 file ID where the generated resume will be uploaded.
    '''
    local_file_path = None
    service = get_resume_generation_service()
    s3 = ObjectStorage()

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            local_file_path = temp_file.name
        temp_file.close()

        # generate resume
        output_path = service.generate(
            user_id= f"{self.request.id}",
            job_data= job_data,
            output_path= local_file_path
        )

        # Upload the file to object store
        if not s3.upload_file(
            file_id= file_id,
            file_path= output_path
        ):
            self.update_state(
                state="FAILURE",
                meta=failure_meta(
                    message=f" Failed to upload generated resume to S3 for file_id:{file_id} ",
                    error="S3UploadError"
            ))
            raise Ignore()  # permanent failure, no retries
        
        """
        pending improvement:
        [ ] Files are being generated On demand, Consider Updating the "job_data" table for quick download next time.
        [ ] If not, add expiration policy for file.
        """

        # success response
        payload = file_payload(
            file_id= file_id,
            download_url= s3.get_public_url(file_id)
        )
        self.update_state(
            state='SUCCESS', 
            meta= success_meta(
                message="Resume generated and uploaded successfully",
                result= payload
            ))
        return payload
    
    except Exception as e:
        raise CustomException(f"Unexpected error generating resume for file_id={file_id}: {e}", status_code=500)
    
    finally:
        # file cleanup
        os.remove(local_file_path) if local_file_path and os.path.exists(local_file_path) else None
