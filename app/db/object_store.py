from functools import lru_cache
import json
from boto3 import client
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

from app.core.logger import db_logger as logger
from app.core.exception import CustomException
from app.core.config import S3Settings


@lru_cache()
def get_s3_client(S3_config: S3Settings = S3Settings()) -> client:
    ''' 
    Returns Object Store (S3) client instance 
    Args:
        url:str - Objectstore url that is reachable,
    '''
    
    try:
        s3_client = client(
            service_name='s3',
            aws_access_key_id= S3_config.ACCESS_KEY,
            aws_secret_access_key= S3_config.SECRET_KEY,
            region_name= S3_config.REGION_NAME,
            endpoint_url= S3_config.INTERNAL_ENDPOINT_URL,
            config = Config(
                signature_version="s3v4",
            ),
        )

        logger.info("S3 client created")
        return s3_client

    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error("S3 credentials error: %s", e)
        raise CustomException("S3 credentials are not properly configured.")


def ensure_bucket_exists(S3_config: S3Settings = S3Settings()) -> None:
    """ Create Bucket if not exist. - App startup"""
    storage = get_s3_client(S3_config)

    try:
        # check is bucket exist
        storage.head_bucket(Bucket=S3_config.BUCKET_NAME)
        logger.info(f"Bucket '{S3_config.BUCKET_NAME}' already exists. ")
    
    except ClientError as exe:
        error_code = exe.response["Error"]["Code"]

        if error_code in ("404", "NoSuchBucket"):
            logger.warning(f"Bucket '{S3_config.BUCKET_NAME}' not found, Creating new bucket.")
            print(f" [*] No Bucket found, Creating new bucket '{S3_config.BUCKET_NAME}' ")

            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AddPublicReadPermissions",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{S3_config.BUCKET_NAME}/*"]
                    }
                ]
            }
            # create New bucket
            try:
                storage.create_bucket(Bucket=S3_config.BUCKET_NAME)
                storage.put_bucket_policy(
                    Bucket= S3_config.BUCKET_NAME,
                    Policy= json.dumps(bucket_policy)
                )
                logger.info(f" Bucket {S3_config.BUCKET_NAME} created.")
                print(f" [*] Bucket {S3_config.BUCKET_NAME} created.")
                
            except Exception as e:
                raise CustomException(f" Error occured while creating bucker ", str(e))
            
        else:
            raise CustomException(f" Unexpected error while checking the state of Bucket {S3_config.BUCKET_NAME}")
