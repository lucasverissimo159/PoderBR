from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import affordability, health
from app.core.config import settings
from app.core.exceptions import DomainException, domain_exception_handler


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Purchasing Power Intelligence API",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(DomainException, domain_exception_handler)

    # Routers
    app.include_router(health.router, tags=["System"])
    app.include_router(
        affordability.router, prefix=settings.API_V1_STR, tags=["Analytics"]
    )

    return app


app = create_app()
