"""
UniManage – AWS Integration Services
====================================
This module provides ready-to-use hooks and connection helpers for:
  - Amazon S3: Profile photo upload, deletion, pre-signed URLs
  - Amazon RDS: Connection pool health check and credentials
  - Amazon EC2 / VPC: Instance metadata and network validation
"""

import os
import logging

logger = logging.getLogger("UniManage.AWS")

# Optional boto3 import with graceful fallback
try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logger.warning("boto3 is not installed. Running in mock/local mode.")


class S3StorageService:
    """
    Amazon S3 Integration Service for handling student profile photos.
    """

    def __init__(self, bucket_name=None, region_name=None):
        self.bucket = bucket_name or os.getenv("S3_BUCKET", "unimanage-profiles")
        self.region = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.s3_client = None

        if BOTO3_AVAILABLE:
            try:
                self.s3_client = boto3.client(
                    "s3",
                    region_name=self.region,
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID") or None,
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY") or None,
                )
            except Exception as e:
                logger.warning(f"Could not initialize S3 client: {e}")

    def upload_profile_image(self, file_stream, filename, content_type="image/jpeg"):
        """
        Uploads an image file object directly to Amazon S3.
        Returns:
            str: Public or S3 URL of the uploaded object
        """
        if not self.s3_client:
            logger.info(f"[Mock S3] Uploading {filename} to bucket '{self.bucket}'")
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/uploads/{filename}"

        key = f"uploads/{filename}"
        try:
            self.s3_client.upload_fileobj(
                file_stream,
                self.bucket,
                key,
                ExtraArgs={
                    "ContentType": content_type,
                    "ACL": "public-read"  # Or use pre-signed URLs if bucket is private
                }
            )
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except (ClientError, NoCredentialsError) as e:
            logger.error(f"S3 Upload failed: {e}")
            raise e

    def generate_presigned_url(self, object_key, expiration=3600):
        """
        Generates a secure temporary pre-signed URL for private S3 objects.
        """
        if not self.s3_client:
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{object_key}"

        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": object_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL: {e}")
            return None

    def delete_profile_image(self, object_key):
        """
        Deletes a profile image from Amazon S3.
        """
        if not self.s3_client:
            logger.info(f"[Mock S3] Deleted {object_key}")
            return True

        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=object_key)
            return True
        except ClientError as e:
            logger.error(f"S3 Delete failed: {e}")
            return False


class RDSHealthChecker:
    """
    Amazon RDS MySQL Health & Diagnostic Helper
    """

    @staticmethod
    def get_connection_info():
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "database": os.getenv("DB_NAME", "unimanage"),
            "user": os.getenv("DB_USER", "root"),
            "is_rds": "rds.amazonaws.com" in os.getenv("DB_HOST", "")
        }


# Singleton instance ready for import in app.py
s3_service = S3StorageService()

