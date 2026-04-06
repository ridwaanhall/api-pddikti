from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.middleware import APIStatusMiddleware, SEOHeadersMiddleware
from app.web.router import router as web_router


app = FastAPI(
    title="PDDIKTI API",
    description=(
        "Provides structured access to data from Pangkalan Data Pendidikan Tinggi "
        "(PDDikti), Indonesia's Higher Education Database"
    ),
    version="4.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

app.add_middleware(SEOHeadersMiddleware)
app.add_middleware(APIStatusMiddleware)

app.include_router(api_router)
app.include_router(web_router)
