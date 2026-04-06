from typing import Annotated

from fastapi import APIRouter
from fastapi import Path

from app.api.common import api_client, as_json


router = APIRouter(tags=["mahasiswa"])

MahasiswaIdParam = Annotated[
    str,
    Path(
        title="Student ID",
        description="Unique identifier of the student (Mahasiswa).",
        min_length=1,
    ),
]


@router.get(
    "/mhs/detail/{id_mhs}/",
    summary="Get student detail",
    description="Return profile and academic status details for a student.",
)
def mhs_detail(id_mhs: MahasiswaIdParam):
    return as_json(api_client.get_with_keyword("detail/mhs", id_mhs))


ENDPOINT_GROUP = {
    "id": "mahasiswa",
    "label": "Students (Mahasiswa)",
    "description": "Endpoints for student profile and status detail.",
    "endpoints": [
        {"method": "GET", "path": "/api/mhs/detail/{id_mhs}/", "summary": "Get student detail"},
    ],
}
