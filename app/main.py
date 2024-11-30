from fastapi import FastAPI

from app.core.config import settings_v1
from app.v1.api.endpoints.files import router_v1
from app.db.session import Base, engine
from app.core.setup_logging import logger_v1


def create_app() -> FastAPI:
    """Create and configure a FastAPI application.

    `Description`:
        This function initializes the application settings,
        checks if the storage exists, creates all database tables,
        and and mounts API versions as sub-applications.

    `Returns`:
        **FastAPI**: Main FastAPI application instance with all versions.
    """
    try:
        logger_v1.debug('The application is launched...')
        Base.metadata.create_all(bind=engine)
        app = FastAPI(
            title=settings_v1.APP_TITLE,
            version=settings_v1.APP_VERSION,
            description=settings_v1.APP_DESCRIPTION,
            docs_url=settings_v1.DOCS_URL,
            redoc_url=settings_v1.REDOC_URL,
        )
        logger_v1.debug(f'App: {app.title}[{app.version}] is setup.')
        app.include_router(
            router_v1,
            prefix=settings_v1.ROUTE_PREFIX,
            tags=['Files']
        )
        return app
    except Exception as err:
        logger_v1.critical(f'{err}', exc_info=True)


app = create_app()
