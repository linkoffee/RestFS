import os
from datetime import datetime as dt
from pathlib import Path
from typing import Union, List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File
from app.schemas.file import FileCreate


def create_file(db: Session, file_data: FileCreate) -> File:
    """Locally creates a file with the specified name.

    `Args`:
        db (Session): An object for interacting with the database
        file_data (FileCreate): Data to create a file

    `Returns`:
        File: File with the specified name
    """
    storage_path = Path(settings.FILE_STORAGE_PATH)
    storage_path.mkdir(parents=True, exist_ok=True)

    file_path = storage_path / file_data.fname

    if file_path.exists():
        raise FileExistsError(f'File `{file_data.fname}` already exists.')
    with file_path.open('w') as f:
        f.write('')
    fsize = file_path.stat().st_size
    mdt = dt.now()
    new_file_data = file_data.model_dump()
    new_file_data.update({'fsize': fsize, 'mdt': mdt})
    new_file = File(**new_file_data)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_file(db: Session, file_id: int) -> Union[File, None]:
    """Gets a specific file from the database by its id.

    `Args`:
        db (Session): An object for interacting with the database
        file_id (int): Unique file identifier

    `Returns`:
        Union[File, None]: File if exist, else None
    """
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        return None
    return file


def update_file(db: Session, file_id: int,
                file_data: FileCreate) -> Union[File, None]:
    """Changes the file selected by ID.

    `Args`:
        db (Session): An object for interacting with the database
        file_id (int): Unique file identifier
        file_data (FileCreate): Data to update a file

    `Returns`:
        Union[File, None]: File if exist, else None
    """
    file = get_file(db, file_id)
    if file is None:
        return None
    storage_path = Path(settings.FILE_STORAGE_PATH)
    old_file_path = storage_path / file.fname
    new_file_path = storage_path / file_data.fname

    if file.fname != file_data.fname:
        if old_file_path.exists():
            old_file_path.rename(new_file_path)
        else:
            raise FileNotFoundError(
                f'File `{file.fname}` not found in storage.'
            )

    mdt = dt.now()
    file.fname = file_data.fname
    file.mdt = mdt

    for key, value in file_data.model_dump().items():
        setattr(file, key, value)

    db.commit()
    db.refresh(file)
    return file


def delete_file(db: Session, file_id: int) -> bool:
    """Allows you to delete a file if it was found.

    `Args`:
        db (Session): An object for interacting with the database
        file_id (int): Unique file identifier

    `Returns`:
        bool: True - if the file exists, otherwise False
    """
    file = get_file(db, file_id)
    if not file:
        return False
    file_path = os.path.join(settings.FILE_STORAGE_PATH, file.fname)

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(file)
    db.commit()
    return True


def list_files(db: Session) -> List[File]:
    return db.query(File).all()
