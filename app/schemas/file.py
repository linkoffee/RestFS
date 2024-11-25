from datetime import datetime as dt

from pydantic import BaseModel, Field


class FileBase(BaseModel):
    fname: str = Field(..., min_length=1, description="File name")


class FileCreate(FileBase):
    """Strict validation for file creation."""
    pass


class FileGet(BaseModel):
    """Relaxed validation for file retrieval."""
    id: int
    fname: str
    fsize: int
    mdt: dt

    class Config:
        from_attributes = True
