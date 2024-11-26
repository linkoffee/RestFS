import os
from datetime import datetime as dt
from pathlib import Path
from typing import Union, List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File
from app.schemas.file import FileGet, FileCreate, FileUpdate


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
        if file_data.content:
            f.write(file_data.content)

    fsize = file_path.stat().st_size
    mdt = dt.now()
    new_file_data = file_data.model_dump()
    new_file_data.pop('content', None)
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


def get_file_with_content(db: Session, file_id: int) -> Union[FileGet, None]:
    """Gets file data along with its contents by its id.

    `Args`:
        db (Session): An object for interacting with the database
        file_id (int): Unique file identifier

    `Returns`:
        Union[FileGet, None]: File with actual content if exist, else None
    """
    file = get_file(db, file_id)
    if not file:
        return None
    return FileGet.from_orm(file)


def update_file(db: Session, file_id: int,
                file_data: FileUpdate) -> Union[File, None]:
    """Changes the file selected by ID.

    `Args`:
        db (Session): An object for interacting with the database
        file_id (int): Unique file identifier
        file_data (FileUpdate): Data to update a file

    `Returns`:
        Union[File, None]: File if exist, else None
    """
    file = get_file(db, file_id)
    if file is None:
        return None

    new_fname = file_data.fname if file_data.fname is not None else file.fname
    if file_data.content is not None:
        new_content = file_data.content
    else:
        new_content = Path(
            settings.FILE_STORAGE_PATH, file.fname
        ).read_text()

    if new_fname != file.fname:
        old_path = Path(settings.FILE_STORAGE_PATH, file.fname)
        new_path = Path(settings.FILE_STORAGE_PATH, new_fname)
        old_path.rename(new_path)
        file.fname = new_fname

    file_path = Path(settings.FILE_STORAGE_PATH, file.fname)
    file_path.write_text(new_content)

    file.mdt = dt.now()
    file.fsize = file_path.stat().st_size

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
    """Gets a list of all files.

    `Args`:
        db (Session): An object for interacting with the database

    `Returns`:
        List[File]: List of file objects
    """
    return db.query(File).all()
