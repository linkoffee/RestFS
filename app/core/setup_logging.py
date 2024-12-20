import os
import logging
from logging.handlers import RotatingFileHandler

from app.core.config import settings_v1, Settings


def setup_app_logging(settings: Settings):
    """Configuring logging based on the settings passed."""
    log_file = os.path.join(settings.LOG_DIR, settings.LOG_FILE_APP)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=settings.MAX_LOG_FILE_SIZE,
        backupCount=settings.BACKUP_COUNT,
    )
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s',
        datefmt=settings.LOG_DATEFMT
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(handler)

    return logger


def setup_sqlalchemy_logging(settings: Settings):
    """Configuring SQLAlchemy logging based on the settings passed."""
    sa_log_file = os.path.join(settings.LOG_DIR, settings.LOG_FILE_SQLALCHEMY)
    handler = RotatingFileHandler(
        sa_log_file,
        maxBytes=settings.MAX_LOG_FILE_SIZE,
        backupCount=settings.BACKUP_COUNT,
    )
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s',
        datefmt=settings.SQLALCHEMY_LOG_DATEFMT
    )
    handler.setFormatter(formatter)

    sa_logger = logging.getLogger('sqlalchemy')
    sa_logger.setLevel(settings.SQLALCHEMY_LOG_LEVEL)
    sa_logger.addHandler(handler)
    sa_logger.propagate = False

    if settings.SQLALCHEMY_ECHO:
        sa_logger.info('SQLAlchemy echo mode: Enabled')
    else:
        sa_logger.info('SQLAlchemy echo mode: Disabled')


logger_v1 = setup_app_logging(settings_v1)
setup_sqlalchemy_logging(settings_v1)
