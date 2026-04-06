from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["prodi"])


@router.get("/prodi/detail/{id_prodi}/", summary="Get study program detail")
def prodi_detail(id_prodi: str):
    return as_json(api_client.get_with_keyword("prodi/detail", id_prodi))


@router.get("/prodi/desc/{id_prodi}/", summary="Get study program description")
def prodi_desc(id_prodi: str):
    return as_json(api_client.get_with_keyword("prodi/desc", id_prodi))


@router.get("/prodi/num-students-lecturers/{id_prodi}/", summary="Get student and lecturer counts")
def prodi_jumlah_mhs_dosen(id_prodi: str):
    return as_json(api_client.get_with_keyword("prodi/num-students-lecturers", id_prodi))


@router.get("/prodi/riwayat/{id_prodi}/", summary="Get study program name history")
def prodi_riwayat(id_prodi: str):
    return as_json(api_client.get_with_keyword("prodi/name-histories", id_prodi))


@router.get("/prodi/biaya-kuliah/{id_prodi}/", summary="Get study program tuition range")
def prodi_biaya_kuliah(id_prodi: str):
    return as_json(api_client.get_with_keyword("prodi/cost-range", id_prodi))


@router.get("/prodi/dosen-homebase/{id_prodi}/{id_thsmt}/", summary="Get homebase lecturers by semester")
def prodi_dosen_homebase(id_prodi: str, id_thsmt: str):
    return as_json(
        api_client.get_with_id_and_param_semester("dosen/homebase", id_prodi, id_thsmt)
    )


@router.get(
    "/prodi/dosen-penghitung-ratio/{id_prodi}/{id_thsmt}/",
    summary="Get lecturers used for ratio calculations",
)
def prodi_dosen_penghitung_ratio(id_prodi: str, id_thsmt: str):
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
