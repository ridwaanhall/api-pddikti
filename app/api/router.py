from fastapi import APIRouter

from app.api.routes import (
    dosen,
    mahasiswa,
    overview,
    prodi,
    prodi_bidang_ilmu,
    pt,
    search,
    stats,
)


router = APIRouter(prefix="/api")

for subrouter in (
    overview.router,
    search.router,
    pt.router,
    prodi.router,
    dosen.router,
    mahasiswa.router,
    stats.router,
    prodi_bidang_ilmu.router,
):
    router.include_router(subrouter)


API_ENDPOINT_CATALOG = [
    overview.ENDPOINT_GROUP,
    search.ENDPOINT_GROUP,
    pt.ENDPOINT_GROUP,
    prodi.ENDPOINT_GROUP,
    dosen.ENDPOINT_GROUP,
    mahasiswa.ENDPOINT_GROUP,
    stats.ENDPOINT_GROUP,
    prodi_bidang_ilmu.ENDPOINT_GROUP,
]


def iter_all_api_endpoints() -> list[dict[str, str]]:
    return [
        endpoint
        for group in API_ENDPOINT_CATALOG
        for endpoint in group["endpoints"]
    ]
