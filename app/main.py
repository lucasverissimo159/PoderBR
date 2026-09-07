from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.api.routes import affordability, health, quality
from app.core.config import settings
from app.core.exceptions import DomainException, domain_exception_handler
from app.core.logging import setup_logging
from app.core.security import limiter


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Purchasing Power Intelligence API",
    )

    # Security Headers
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "OPTIONS"],  # Restrict to strictly read-only for public endpoints
        allow_headers=["*"],
    )

    # Rate Limiting
    app.state.limiter = limiter

    # Exception Handlers
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Routers
    app.include_router(health.router, tags=["System"])
    app.include_router(
        affordability.router, prefix=settings.API_V1_STR, tags=["Analytics"]
    )
    app.include_router(
        quality.router, prefix=f"{settings.API_V1_STR}/quality", tags=["Observability"]
    )

    return app


app = create_app()
