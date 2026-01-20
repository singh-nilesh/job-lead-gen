import os
import tempfile
from app.core.exception import CustomException
from app.db.s3_adapters import ObjectStorage
from app.services.cover_letter import CoverLetterService
from app.core.celery_config import celery_app
from celery.exceptions import Ignore
from app.tasks.interface import failure_meta, success_meta, file_payload
import asyncio


@celery_app.task(bind=True)
def generate_cover_letter(self, user_id: str, job_data: str, personalization_input:str, file_id:str) -> None:
    """ Completes the cover letter generation task."""

    # Celery with asyncio setup
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    service = CoverLetterService()
    s3 = ObjectStorage()
    local_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            local_file_path = temp_file.name
        temp_file.close()

        # Generate cover letter
        output_path = loop.run_until_complete(
            service.generate_from_text(
                user_id= user_id,
                job_data= job_data,
                file_path=  local_file_path,
                user_personalized_input= personalization_input
            )
        )

        # Upload generated cover letter to S3
        if not s3.upload_file(
            file_id=file_id,
            file_path=output_path
        ):
            self.update_state(
                state="FAILURE",
                meta=failure_meta(
                    message=f" Failed to upload generated cover letter to S3 for file_id:{file_id} ",
                    error="S3UploadError"
            ))
            raise Ignore()  # permanent failure, no retries
        
        # success response
        payload = file_payload(
            file_id= file_id,
            download_url= s3.get_public_url(file_id)
        )
        self.update_state(
            state='SUCCESS', 
            meta= success_meta(
                message="Cover letter generated and uploaded successfully",
                result = payload
            ))
        return payload
       
    except Exception as e:
        raise CustomException(f"An unexpected error occurred for task_id:{self.request.id} | file_id:{file_id}: {str(e)}")
    
    finally:
        # file cleanup
        os.remove(local_file_path) if local_file_path and os.path.exists(local_file_path) else None
        loop.close()