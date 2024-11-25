import os


class Settings:
    """RestFS Settings."""

    APP_TITLE = 'RestFS'
    APP_VERSION = '1.0'
    APP_DESCIPTION = 'Microservice using fastapi and sqlalchemy libs.'
    DB_URL = 'sqlite:///./restfs.db'
    FILE_STORAGE_PATH = os.path.abspath('./storage')
    ROUTE_PREFIX = '/files'

    @staticmethod
    def is_storage_exist():
        """Checks if the repository exists, otherwise creates it."""
        if not os.path.exists(Settings.FILE_STORAGE_PATH):
            os.makedirs(Settings.FILE_STORAGE_PATH)


settings = Settings()
