from pathlib import Path
from fastapi import HTTPException

from app.core.config import settings_v1
from app.core.setup_logging import logger_v1

# Absolute path to storage dir
BASE_DIR = Path(settings_v1.FILE_STORAGE_PATH).resolve()


def secure_path(fname: str) -> Path:
    """Creates a safe path to the file and checks if it is in storage.

    `Args`:
        **fname (str)**: Name of the file

    `Raises`:
        **HTTPException**: 403 (Access Denied)

    `Returns`:
        **Path**: Path to file in storage dir
    """
    try:
        file_path = (BASE_DIR / fname).resolve()
        if not str(file_path).startswith(str(BASE_DIR)):
            logger_v1.warning(
                f'Access denied to path: `{file_path}`. '
                'Outside of storage dir.'
            )
            raise HTTPException(
                status_code=403,
                detail='Access to this path is forbidden.'
            )
        logger_v1.info(f'Secure path created: `{file_path}`.')
        return file_path
    except Exception as err:
        logger_v1.error(f'{err}', exc_info=True)
