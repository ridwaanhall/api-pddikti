from typing import Annotated

from fastapi import APIRouter
from fastapi import Path

from app.api.common import api_client, as_json


router = APIRouter(tags=["prodi"])

ProdiIdParam = Annotated[
    str,
    Path(
        title="Study Program ID",
        description="Unique identifier of the study program (Prodi).",
        min_length=1,
    ),
]
SemesterParam = Annotated[
    str,
    Path(
        title="Semester ID",
        description="Semester code used for period-based Prodi queries.",
        min_length=1,
    ),
]


@router.get(
    "/prodi/detail/{id_prodi}/",
    summary="Get study program detail",
    description="Return detailed information about a specific study program.",
)
def prodi_detail(id_prodi: ProdiIdParam):
    return as_json(api_client.get_with_keyword("prodi/detail", id_prodi))


@router.get(
    "/prodi/desc/{id_prodi}/",
    summary="Get study program description",
    description="Return narrative description and profile details of the study program.",
)
def prodi_desc(id_prodi: ProdiIdParam):
    return as_json(api_client.get_with_keyword("prodi/desc", id_prodi))


@router.get(
    "/prodi/num-students-lecturers/{id_prodi}/",
    summary="Get student and lecturer counts",
    description="Return the number of students and lecturers associated with a study program.",
)
def prodi_jumlah_mhs_dosen(id_prodi: ProdiIdParam):
    return as_json(api_client.get_with_keyword("prodi/num-students-lecturers", id_prodi))


@router.get(
    "/prodi/riwayat/{id_prodi}/",
    summary="Get study program name history",
    description="Return historical naming records for a study program.",
)
def prodi_riwayat(id_prodi: ProdiIdParam):
    return as_json(api_client.get_with_keyword("prodi/name-histories", id_prodi))


@router.get(
    "/prodi/biaya-kuliah/{id_prodi}/",
    summary="Get study program tuition range",
    description="Return tuition range information for a study program.",
)
def prodi_biaya_kuliah(id_prodi: ProdiIdParam):
    return as_json(api_client.get_with_keyword("prodi/cost-range", id_prodi))


@router.get(
    "/prodi/dosen-homebase/{id_prodi}/{id_thsmt}/",
    summary="Get homebase lecturers by semester",
    description="Return lecturers with homebase assignments in the study program for a semester.",
)
def prodi_dosen_homebase(id_prodi: ProdiIdParam, id_thsmt: SemesterParam):
    return as_json(
        api_client.get_with_id_and_param_semester("dosen/homebase", id_prodi, id_thsmt)
    )


@router.get(
    "/prodi/dosen-penghitung-ratio/{id_prodi}/{id_thsmt}/",
    summary="Get lecturers used for ratio calculations",
    description="Return lecturers included in ratio calculations for a study program and semester.",
)
def prodi_dosen_penghitung_ratio(id_prodi: ProdiIdParam, id_thsmt: SemesterParam):
    return as_json(
        api_client.get_with_id_and_param_semester(
            "dosen/penghitung-ratio", id_prodi, id_thsmt
        )
    )


ENDPOINT_GROUP = {
    "id": "prodi",
    "label": "Study Programs (Prodi)",
    "description": "Endpoints for study program detail and academic metrics.",
    "endpoints": [
        {"method": "GET", "path": "/api/prodi/detail/{id_prodi}/", "summary": "Get study program detail"},
        {"method": "GET", "path": "/api/prodi/desc/{id_prodi}/", "summary": "Get study program description"},
        {"method": "GET", "path": "/api/prodi/num-students-lecturers/{id_prodi}/", "summary": "Get student and lecturer counts"},
        {"method": "GET", "path": "/api/prodi/riwayat/{id_prodi}/", "summary": "Get study program name history"},
        {"method": "GET", "path": "/api/prodi/biaya-kuliah/{id_prodi}/", "summary": "Get study program tuition range"},
        {"method": "GET", "path": "/api/prodi/dosen-homebase/{id_prodi}/{id_thsmt}/", "summary": "Get homebase lecturers by semester"},
        {"method": "GET", "path": "/api/prodi/dosen-penghitung-ratio/{id_prodi}/{id_thsmt}/", "summary": "Get lecturers used for ratio calculations"},
    ],
}
