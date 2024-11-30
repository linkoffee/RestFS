import os
import configparser


class Settings:
    """RestFS Settings."""

    def __init__(self, config_file='app/core/app_conf.ini', version='v1'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.version = version
        self.load_logging_settings()
        self.load_app_settings()
        self.load_sqlalchemy_settings()
        self.setup_storage()

    def load_logging_settings(self):
        """Loading general logging settings."""
        logging_config = self.config['logging']
        core_dir = os.path.abspath(os.path.dirname(__file__))
        self.LOG_LEVEL = logging_config.get('log_level', 'INFO')
        self.LOG_DIR = os.path.join(
            core_dir, logging_config.get('log_dir', 'logs')
        )
        self.LOG_FILE_APP = logging_config.get(
            'log_file_app', 'restfs-app.log'
        )
        self.LOG_FILE_SQLALCHEMY = logging_config.get(
            'lof_file_sqlalchemy', 'sqlalchemy.log'
        )
        self.MAX_LOG_FILE_SIZE = int(
            logging_config.get('max_log_file_size', 10485760)
        )
        self.BACKUP_COUNT = int(logging_config.get('backup_count', 3))

        os.makedirs(self.LOG_DIR, exist_ok=True)

    def load_app_settings(self):
        """Loading application settings for a specific API version."""
        section_name = f'restfs-app-{self.version}'
        if section_name not in self.config:
            raise ValueError(
                f'Config section `{section_name}` '
                f'not found for version `{self.version}`'
            )
        app_config = self.config[section_name]
        self.APP_TITLE = app_config.get('app_title')
        self.APP_VERSION = app_config.get('app_version')
        self.APP_DESCRIPTION = app_config.get('app_description')
        self.DOCS_URL = app_config.get('docs_url')
        self.REDOC_URL = app_config.get('redoc_url')
        self.DB_URL = app_config.get('db_url')
        self.FILE_STORAGE_PATH = os.path.abspath(
            app_config.get('file_storage_path')
        )
        self.ROUTE_PREFIX = app_config.get('route_prefix')

    def load_sqlalchemy_settings(self):
        """Loading Sqlalchemy settings."""
        sqlalchemy_config = self.config['sqlalchemy']
        self.SQLALCHEMY_LOG_LEVEL = sqlalchemy_config.get('log_level', 'INFO')
        self.SQLALCHEMY_ECHO = sqlalchemy_config.getboolean('echo', False)

    def setup_storage(self):
        """Checks if the repository exists, otherwise creates it."""
        if not os.path.exists(self.FILE_STORAGE_PATH):
            os.makedirs(self.FILE_STORAGE_PATH)


settings_v1 = Settings(version='v1')
