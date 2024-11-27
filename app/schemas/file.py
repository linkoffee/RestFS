from typing import Optional
from pathlib import Path
from datetime import datetime as dt

from pydantic import BaseModel, Field

from app.core.config import settings
from app.models.file import File


class FileCreate(BaseModel):
    """Strict validation for file creation."""
    fname: str = Field(..., min_length=1, description="File name")
    content: Optional[str] = None


class FileGet(BaseModel):
    """Relaxed validation for file retrieval."""
    id: int
    fname: str
    fsize: int
    mdt: dt
    content: Optional[str] = None

    @classmethod
    def from_orm(cls, file: File) -> 'FileGet':
        """Creates an object of class `FileGet` from an orm model object.

        Args:
            file (File): ORM model object.

        Returns:
            FileGet: Serializer for retrieve file object.
        """
        file_path = Path(settings.FILE_STORAGE_PATH) / file.fname
        fsize = file_path.stat().st_size if file_path.exists() else 0
        content = file_path.read_text() if file_path.exists() else None

        return cls(
            id=file.id,
            fname=file.fname,
            fsize=fsize,
            mdt=file.mdt,
            content=content
        )


class FileUpdate(BaseModel):
    """Relaxed validation for file updating."""
    fname: Optional[str] = None
    content: Optional[str] = None
