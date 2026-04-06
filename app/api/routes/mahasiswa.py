from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["mahasiswa"])


@router.get("/mhs/detail/{id_mhs}/", summary="Get student detail")
def mhs_detail(id_mhs: str):
    return as_json(api_client.get_with_keyword("detail/mhs", id_mhs))


ENDPOINT_GROUP = {
    "id": "mahasiswa",
    "label": "Students (Mahasiswa)",
    "description": "Endpoints for student profile and status detail.",
    "endpoints": [
        {"method": "GET", "path": "/api/mhs/detail/{id_mhs}/", "summary": "Get student detail"},
    ],
}
