from typing import Annotated

from fastapi import APIRouter
from fastapi import Path

from app.api.common import api_client, as_json


router = APIRouter(tags=["search"])

KeywordParam = Annotated[
    str,
    Path(
        title="Search keyword",
        description="Keyword text used to search PDDIKTI entities.",
        min_length=1,
    ),
]


@router.get(
    "/search/all/{keyword}/",
    summary="Search all entities",
    description="Search universities, study programs, lecturers, and students in one request.",
)
def search_all(keyword: KeywordParam):
    return as_json(api_client.get_with_keyword("pencarian/all", keyword))


@router.get(
    "/search/pt/{keyword}/",
    summary="Search universities",
    description="Search only universities (PT) matching the given keyword.",
)
def search_pt(keyword: KeywordParam):
    return as_json(api_client.get_with_keyword("pencarian/pt", keyword))


@router.get(
    "/search/prodi/{keyword}/",
    summary="Search study programs",
    description="Search study program records (Prodi) by keyword.",
)
def search_prodi(keyword: KeywordParam):
    return as_json(api_client.get_with_keyword("pencarian/prodi", keyword))


@router.get(
    "/search/dosen/{keyword}/",
    summary="Search lecturers",
    description="Search lecturer records (Dosen) by keyword.",
)
def search_dosen(keyword: KeywordParam):
    return as_json(api_client.get_with_keyword("pencarian/dosen", keyword))


@router.get(
    "/search/mhs/{keyword}/",
    summary="Search students",
    description="Search student records (Mahasiswa) by keyword.",
)
def search_mahasiswa(keyword: KeywordParam):
    return as_json(api_client.get_with_keyword("pencarian/mhs", keyword))


ENDPOINT_GROUP = {
    "id": "search",
    "label": "Search",
    "description": "Keyword search across all entity domains.",
    "endpoints": [
        {"method": "GET", "path": "/api/search/all/{keyword}/", "summary": "Search all entities"},
        {"method": "GET", "path": "/api/search/pt/{keyword}/", "summary": "Search universities"},
        {"method": "GET", "path": "/api/search/prodi/{keyword}/", "summary": "Search study programs"},
        {"method": "GET", "path": "/api/search/dosen/{keyword}/", "summary": "Search lecturers"},
        {"method": "GET", "path": "/api/search/mhs/{keyword}/", "summary": "Search students"},
    ],
}
