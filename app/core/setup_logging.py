import os
import logging
from logging.handlers import RotatingFileHandler

from app.core.config import settings_v1, Settings


def setup(settings: Settings):
    """Configuring logging based on the settings passed.

    `Args`:
        **settings (Settings)**: App configuration object

    `Returns`:
        **logger (Logger)**: logger object configured with app settings
    """
    log_file = os.path.join(settings.LOG_DIR, settings.LOG_FILE_APP)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=settings.MAX_LOG_FILE_SIZE,
        backupCount=settings.BACKUP_COUNT,
    )
    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(message)s][%(filename)s][%(lineno)s]'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(handler)

    return logger


logger_v1 = setup(settings_v1)
