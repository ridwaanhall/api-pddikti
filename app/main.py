from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import get_settings
from app.core.middleware import (
    APIStatusMiddleware,
    RequestIdentityMiddleware,
    SEOHeadersMiddleware,
)
from app.web.router import router as web_router


settings = get_settings()


app = FastAPI(
    title="PDDIKTI API",
    description=(
        "Provides structured access to data from Pangkalan Data Pendidikan Tinggi "
        "(PDDikti), Indonesia's Higher Education Database"
    ),
    version=settings.api_version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

app.add_middleware(SEOHeadersMiddleware)
app.add_middleware(APIStatusMiddleware)
app.add_middleware(RequestIdentityMiddleware)

app.include_router(api_router)
app.include_router(web_router)
