from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.endpoints.files import router_v1
from app.db.session import Base, engine


def create_app() -> FastAPI:
    """Create and configure a FastAPI application.

    `Description`: This function initializes the application settings,
    checks if the storage exists, creates all database tables,
    and includes the API router for version 1.

    `Returns`:
        FastAPI: An instance of the FastAPI application
        configured with application settings.
    """
    settings.is_storage_exist()
    Base.metadata.create_all(bind=engine)
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        description=settings.APP_DESCIPTION
    )
    app.include_router(
        router_v1,
        prefix=settings.ROUTE_PREFIX,
        tags=['Files']
    )
    return app


app = create_app()
