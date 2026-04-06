from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["dosen"])


@router.get("/dosen/profile/{id_dosen}/", summary="Get lecturer profile")
def dosen_profile(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/profile", id_dosen))


@router.get("/dosen/study-history/{id_dosen}/", summary="Get lecturer education history")
def dosen_riwayat_pendidikan(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/study-history", id_dosen))


@router.get("/dosen/teaching-history/{id_dosen}/", summary="Get lecturer teaching history")
def dosen_riwayat_mengajar(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/teaching-history", id_dosen))


@router.get("/dosen/penelitian/{id_dosen}/", summary="Get lecturer research portfolio")
def dosen_portofolio_penelitian(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/portofolio/penelitian", id_dosen))


@router.get("/dosen/pengabdian/{id_dosen}/", summary="Get lecturer service portfolio")
def dosen_portofolio_pengabdian(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/portofolio/pengabdian", id_dosen))


@router.get("/dosen/karya/{id_dosen}/", summary="Get lecturer works portfolio")
def dosen_portofolio_karya(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/portofolio/karya", id_dosen))


@router.get("/dosen/paten/{id_dosen}/", summary="Get lecturer patents portfolio")
def dosen_portofolio_paten(id_dosen: str):
    return as_json(api_client.get_with_keyword("dosen/portofolio/paten", id_dosen))


ENDPOINT_GROUP = {
    "id": "dosen",
    "label": "Lecturers (Dosen)",
    "description": "Endpoints for lecturer profile, history, and portfolios.",
    "endpoints": [
        {"method": "GET", "path": "/api/dosen/profile/{id_dosen}/", "summary": "Get lecturer profile"},
        {"method": "GET", "path": "/api/dosen/study-history/{id_dosen}/", "summary": "Get lecturer education history"},
        {"method": "GET", "path": "/api/dosen/teaching-history/{id_dosen}/", "summary": "Get lecturer teaching history"},
        {"method": "GET", "path": "/api/dosen/penelitian/{id_dosen}/", "summary": "Get lecturer research portfolio"},
        {"method": "GET", "path": "/api/dosen/pengabdian/{id_dosen}/", "summary": "Get lecturer service portfolio"},
        {"method": "GET", "path": "/api/dosen/karya/{id_dosen}/", "summary": "Get lecturer works portfolio"},
        {"method": "GET", "path": "/api/dosen/paten/{id_dosen}/", "summary": "Get lecturer patents portfolio"},
    ],
}
