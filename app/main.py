from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.endpoints.files import router_v1
from app.db.session import Base, engine


def create_app() -> FastAPI:
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
