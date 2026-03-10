import boto3
from app.storage.utils import generate_image_key
from app.storage.storage_base import StorageBase
from app.core.config.config import settings

class S3Storage(StorageBase):
    """
    Store images in AWS S3.
    """

    def __init__(self):
        self.bucket_name = settings.BUCKET_NAME
        self.s3 = boto3.client("s3", region_name=settings.AWS_REGION)

    def save_image(self, *, image_bytes: bytes, user_id: int) -> str:
        """
        Upload image bytes to S3 and return the storage key.
        """
        key = generate_image_key(user_id=user_id, extension="jpg")

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=image_bytes,
            ContentType="image/jpeg",
        )

        return key

    def load_image(self, key: str) -> bytes:
        """
        Load an image from S3 and return it as bytes.
        """
        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=key,
        )

        return response["Body"].read()