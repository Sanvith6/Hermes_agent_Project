from minio import Minio
from app.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)


def upload_file(file_data: bytes, file_key: str, content_type: str) -> str:
    minio_client.put_object(
        settings.MINIO_BUCKET,
        file_key,
        file_data,
        length=len(file_data),
        content_type=content_type
    )
    return f"{settings.MINIO_URL}/{settings.MINIO_BUCKET}/{file_key}"
