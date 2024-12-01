from typing import Optional
from pathlib import Path
from datetime import datetime as dt

from pydantic import BaseModel, Field

from app.core.config import settings_v1
from app.core.setup_logging import logger_v1
from app.v1.models.file import File


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

        `Args`:
            **file (File)**: ORM model object.

        `Returns`:
            **FileGet**: Serializer for retrieve file object.
        """
        try:
            file_path = Path(settings_v1.FILE_STORAGE_PATH) / file.fname
            fsize = file_path.stat().st_size if file_path.exists() else 0
            content = file_path.read_text() if file_path.exists() else None

            logger_v1.debug(
                f'Processing file: `{file.fname}`, '
                f'size: `{fsize / 1024:.2f}` Kbytes'
            )

            return cls(
                id=file.id,
                fname=file.fname,
                fsize=fsize,
                mdt=file.mdt,
                content=content
            )
        except Exception as err:
            logger_v1.error(
                f'Error processing file `{file.fname}`. {err}',
                exc_info=True
            )


class FileUpdate(BaseModel):
    """Relaxed validation for file updating."""
    fname: Optional[str] = None
    content: Optional[str] = None
