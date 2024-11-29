from pathlib import Path
from fastapi import HTTPException

from app.core.config import settings

# Absolute path to storage dir
BASE_DIR = Path(settings.FILE_STORAGE_PATH).resolve()


def secure_path(fname: str) -> Path:
    """Creates a safe path to the file and checks if it is in storage.

    `Args`:
        **fname (str)**: Name of the file

    `Raises`:
        **HTTPException**: 403 (Access Denied)

    `Returns`:
        **Path**: Path to file in storage dir
    """
    file_path = (BASE_DIR / fname).resolve()
    if not str(file_path).startswith(str(BASE_DIR)):
        raise HTTPException(
            status_code=403,
            detail='Access to this path is forbidden.'
        )
    return file_path
