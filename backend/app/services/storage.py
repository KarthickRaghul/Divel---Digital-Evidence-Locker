import boto3
import os
import logging
from typing import BinaryIO, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # We initialize the client but check env vars before using
        self.s3_client = None
        self.bucket_name = settings.S3_BUCKET_NAME
        
        if settings.AWS_ACCESS_KEY_ID:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )

    def upload_file(self, file_obj: BinaryIO, filename: str, content_type: str) -> str:
        if self.s3_client:
            try:
                self.s3_client.upload_fileobj(
                    file_obj,
                    self.bucket_name,
                    filename,
                    ExtraArgs={'ContentType': content_type}
                )
                return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            except Exception as e:
                logger.error(f"Error uploading to S3: {e}")
                # Fallback to local? For now, re-raise or return None
                raise e
        else:
            # Local Storage Mock
            local_path = f"uploads/{filename}"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(file_obj.read())
            return local_path

    def get_file(self, filename: str) -> Optional[bytes]:
        """
        Retrieve a file from storage.
        Returns the file content as bytes, or None if not found.
        """
        if self.s3_client:
            try:
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
                return response['Body'].read()
            except Exception as e:
                logger.error(f"Error retrieving file from S3: {e}")
                return None
        else:
            # Local Storage
            local_path = f"uploads/{filename}"
            if os.path.exists(local_path):
                with open(local_path, "rb") as f:
                    return f.read()
            else:
                logger.warning(f"File not found in local storage: {local_path}")
                return None
    
    def get_file_url(self, filename: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary file access.
        Useful for serving files to frontend without exposing AWS credentials.
        """
        if self.s3_client:
            try:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': filename},
                    ExpiresIn=expiration
                )
                return url
            except Exception as e:
                logger.error(f"Error generating presigned URL: {e}")
                return None
        else:
            # Return local file path
            return f"/uploads/{filename}"

storage = StorageService()
