from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["statistics"])

# PDDikti retired the whole `visualisasi/*` dataset along with `mahasiswa/count` and
# `dosen/count`; those paths now 404 upstream with no replacement, so the endpoints that
# wrapped them have been removed. What remains below is the set that still returns data.


@router.get(
    "/stats/mhs-count-active/",
    summary="Get active student count",
    description="Return aggregate count of active students.",
)
def mhs_count_active():
    return as_json(api_client.get("mahasiswa/count-active"))


@router.get(
    "/stats/dosen-count-active/",
    summary="Get active lecturer count",
    description="Return aggregate count of active lecturers.",
)
def dosen_count_active():
    return as_json(api_client.get("dosen/count-active"))


@router.get(
    "/stats/pt-count/",
    summary="Get total university count",
    description="Return aggregate count of universities.",
)
def pt_count():
    return as_json(api_client.get("pt/count"))


@router.get(
    "/stats/prodi-count/",
    summary="Get total study program count",
    description="Return aggregate count of study programs.",
)
def prodi_count():
    return as_json(api_client.get("prodi/count"))


@router.get(
    "/stats/prodi-count-bidang-ilmu-terbanyak/",
    summary="Get most common study program field",
    description="Return dominant scientific fields among study programs.",
)
def prodi_bidang_ilmu_terbanyak_count():
    return as_json(api_client.get("prodi/bidang-ilmu"))


ENDPOINT_GROUP = {
    "id": "statistics",
    "label": "Statistics",
    "description": "Aggregate counts across universities, programs, lecturers, and students.",
    "endpoints": [
        {"method": "GET", "path": "/api/stats/mhs-count-active/", "summary": "Get active student count"},
        {"method": "GET", "path": "/api/stats/dosen-count-active/", "summary": "Get active lecturer count"},
        {"method": "GET", "path": "/api/stats/pt-count/", "summary": "Get total university count"},
        {"method": "GET", "path": "/api/stats/prodi-count/", "summary": "Get total study program count"},
        {"method": "GET", "path": "/api/stats/prodi-count-bidang-ilmu-terbanyak/", "summary": "Get most common study program field"},
    ],
}
