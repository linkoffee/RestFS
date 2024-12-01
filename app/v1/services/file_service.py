from datetime import datetime as dt
from typing import Union, List

from sqlalchemy.orm import Session

from app.v1.models.file import File
from app.v1.schemas.file import FileGet, FileCreate, FileUpdate
from app.v1.utils.security import secure_path
from app.core.setup_logging import logger_v1


def create_file(db: Session, file_data: FileCreate) -> File:
    """Locally creates a file with the specified name.

    `Args`:
        **db (Session)**: An object for interacting with the database
        **file_data (FileCreate)**: Data to create a file

    `Returns`:
        **File**: File with the specified name
    """
    try:
        file_path = secure_path(file_data.fname)

        if file_path.exists():
            logger_v1.warning(f'File `{file_data.fname}` already exists.')
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
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)


def get_file(db: Session, file_id: int) -> Union[File, None]:
    """Gets a specific file from the database by its id.

    `Args`:
        **db (Session)**: An object for interacting with the database
        **file_id (int)**: Unique file identifier

    `Returns`:
        **Union[File, None]**: File if exist, else None
    """
    try:
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            return None
        return file
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)


def get_file_with_content(db: Session, file_id: int) -> Union[FileGet, None]:
    """Gets file data along with its contents by its id.

    `Args`:
        **db (Session)**: An object for interacting with the database
        **file_id (int)**: Unique file identifier

    `Returns`:
        **Union[FileGet, None]**: File with actual content if exist, else None
    """
    try:
        file = get_file(db, file_id)
        if not file:
            return None
        return FileGet.from_orm(file)
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)


def update_file(db: Session, file_id: int,
                file_data: FileUpdate) -> Union[File, None]:
    """Changes the file selected by ID.

    `Args`:
        **db (Session)**: An object for interacting with the database
        **file_id (int)**: Unique file identifier
        **file_data (FileUpdate)**: Data to update a file

    `Returns`:
        **Union[File, None]**: File if exist, else None
    """
    try:
        file = get_file(db, file_id)
        if file is None:
            return None

        old_file_path = secure_path(file.fname)
        if file_data.fname:
            new_file_path = secure_path(file_data.fname)
        else:
            new_file_path = old_file_path

        if file_data.content is not None:
            new_content = file_data.content
        else:
            new_content = old_file_path.read_text()

        if new_file_path != old_file_path:
            old_file_path.rename(new_file_path)
            file.fname = new_file_path.name

        new_file_path.write_text(new_content)

        file.mdt = dt.now()
        file.fsize = new_file_path.stat().st_size

        db.commit()
        db.refresh(file)
        return file
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)


def delete_file(db: Session, file_id: int) -> bool:
    """Allows you to delete a file if it was found.

    `Args`:
        **db (Session)**: An object for interacting with the database
        **file_id (int)**: Unique file identifier

    `Returns`:
        **bool**: True - if the file exists, otherwise False
    """
    try:
        file = get_file(db, file_id)
        if not file:
            return False
        file_path = secure_path(file.fname)

        if file_path.exists():
            file_path.unlink()

        db.delete(file)
        db.commit()
        return True
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)


def list_files(db: Session) -> List[File]:
    """Gets a list of all files.

    `Args`:
        **db (Session)**: An object for interacting with the database

    `Returns`:
        **List[File]**: List of file objects
    """
    try:
        return db.query(File).all()
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)
