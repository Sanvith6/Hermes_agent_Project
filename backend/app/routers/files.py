from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from minio import Minio
from app.core.config import settings
from uuid import uuid4
import os

router = APIRouter()

# Initialize MinIO
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate file size (16MB limit)
    contents = await file.read()
    if len(contents) > 16 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 16MB)")

    # Upload to MinIO
    file_key = f"uploads/{current_user.id}/{uuid4()}_{file.filename}"
    minio_client.put_object(
        settings.MINIO_BUCKET,
        file_key,
        contents,
        length=len(contents),
        content_type=file.content_type
    )

    file_url = f"{settings.MINIO_URL}/{settings.MINIO_BUCKET}/{file_key}"

    return {"url": file_url, "key": file_key}
