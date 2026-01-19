"""
This file contains, Adapters for operation on s3 compatible adapters (aws-s3, minio, DigitalOcean) etc.
"""

from app.db.object_store import get_s3_client
from app.core.config import S3Settings
from app.core.exception import ServiceException
from app.core.logger import db_logger as logger
import os
from pathlib import Path


class ObjectStorage:
    """ S3 Object storage adapter for file operations. """
    def __init__(self):
        super().__init__()
        self.s3_config = S3Settings()
        self.s3_client = get_s3_client(self.s3_config)
        if not self.s3_client:
            raise ServiceException(" Unable to create S3 client instance.", logger=logger, status_code=500)
    

    # upload
    def upload_file(self, file_path: str, file_id: str) -> bool:
        """ Upload file from local file path to S3 object storage. """
        logger.info(f"File upload request for '{file_id}'")
        try:
            # check if file exist, is reachable
            local = Path(file_path)
            if not local.is_file():
                logger.error(f"File '{file_path}' not found for upload.")
                return False
            
            self.s3_client.upload_file(
                Filename=str(local),
                Bucket= self.s3_config.BUCKET_NAME,
                Key=file_id
            )
            logger.info(f"File {file_id} uploaded successfully.")
            return True
        
        except Exception as e:
            logger.error(f"Failed file upload. error: {str(e)}")
            return False
    
    def upload_fileobj(self, file_obj:bytes , file_id: str) -> bool:
        """ Upload file from file-like object to S3 object storage. """
        logger.info(f"File upload request for '{file_id}'")
        try:
            self.s3_client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.s3_config.BUCKET_NAME,
                Key=file_id
            )
            logger.info(f"File {file_id} uploaded successfully.")
            return True
        
        except Exception as e:
            logger.error(f"Failed file upload. error: {str(e)}")
            raise e

    # delete
    def delete(self, file_id: str) -> bool:
        logger.info(f"File delete requested for '{file_id}'")
        try:
            res = self.s3_client.delete_object(
                Bucket=self.s3_config.BUCKET_NAME,
                Key=file_id
            )
            # check if delete marker is true
            if res.get("ResponseMetadata", {}).get("DeleteMarker") is True:
                logger.info(f"File '{file_id}' deleted successfully")
                return True
            else:
                logger.error("Failed to delete file.")
                return False

        except Exception as e:
            logger.error(f"Failed to delete file. error: {str(e)}")
            return False
    
    # Download
    def download(self, file_id: str, download_file_path: str) -> bool:
        logger.info(f"Download of file {file_id} requested")
        try:
            # check is path exist
            target = Path(download_file_path)
            if not target.parent.exists():
                os.makedirs(target.parent, exist_ok=True)

            self.s3_client.download_file(
                Bucket=self.s3_config.BUCKET_NAME,
                Key=file_id,
                Filename=str(target)
            )
            logger.info(f"File {file_id} downloaded successfully, at {download_file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Unable to download file {file_id}, error: {str(e)}")
            return False
    

    # Unsigned URL generation
    def unsigned_url(self, file_id: str, expiration: int = 300) -> str:
        """ Generate public access url for the file stored in object storage. """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.s3_config.BUCKET_NAME,
                    'Key': file_id
                },
                ExpiresIn=expiration
            )
            return presigned_url
        
        except Exception as e:
            logger.error(f"Unable to generate unsigned url for file {file_id}, error: {str(e)}")
            return ""
    
    
    # Public URL generation
    def get_public_url(self, file_id: str, bucket: str = None) -> str:
        """ Get public url for the file stored in object storage. """

        # check is bucket, public endpoint url is set
        if not self.s3_config.PUBLIC_ENDPOINT_URL or not (bucket or self.s3_config.BUCKET_NAME):
            logger.error("S3 public endpoint url or bucket name is not set.")
            return ""
        
        return f"{self.s3_config.PUBLIC_ENDPOINT_URL}/{bucket or self.s3_config.BUCKET_NAME}/{file_id}"