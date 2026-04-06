from typing import Annotated

from fastapi import APIRouter
from fastapi import Path
from fastapi.responses import Response

from app.api.common import api_client, as_json


router = APIRouter(tags=["pt"])

PTIdParam = Annotated[
    str,
    Path(
        title="University ID",
        description="Unique identifier of the university (Perguruan Tinggi).",
        min_length=1,
    ),
]
SemesterParam = Annotated[
    str,
    Path(
        title="Semester ID",
        description="Semester code used for period-based PT queries.",
        min_length=1,
    ),
]


@router.get(
    "/pt/detail/{id_pt}/",
    summary="Get university detail",
    description="Return detailed profile information for a university by ID.",
)
def pt_detail(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/detail", id_pt))


@router.get(
    "/pt/prodi/{id_pt}/{id_thsmt}",
    summary="Get university study programs by semester",
    description="List study programs in a university for the specified semester.",
)
def pt_prodi(id_pt: PTIdParam, id_thsmt: SemesterParam):
    return as_json(api_client.get_with_id_and_semester("pt/prodi", id_pt, id_thsmt))


@router.get(
    "/pt/rasio/{id_pt}/",
    summary="Get lecturer-student ratio by university",
    description="Return lecturer-to-student ratio statistics for a university.",
)
def pt_rasio_dosen_mahasiswa(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/rasio", id_pt))


@router.get(
    "/pt/mahasiswa/{id_pt}/",
    summary="Get university student metrics",
    description="Return student-related metrics for the selected university.",
)
def pt_mean_lulus_maba(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/mahasiswa", id_pt))


@router.get(
    "/pt/waktu-studi/{id_pt}/",
    summary="Get average study duration by university",
    description="Return average study duration metrics for the selected university.",
)
def pt_mean_masa_studi(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/waktu-studi", id_pt))


@router.get(
    "/pt/riwayat/{id_pt}/",
    summary="Get university name history",
    description="Return historical naming records for the selected university.",
)
def pt_riwayat(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/name-histories", id_pt))


@router.get(
    "/pt/biaya-kuliah/{id_pt}/",
    summary="Get tuition range by university",
    description="Return tuition fee range information for the selected university.",
)
def pt_biaya_kuliah(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/cost-range", id_pt))


@router.get(
    "/pt/fasilitas/{id_pt}/",
    summary="Get university facilities metadata",
    description="Return facilities and infrastructure metadata for the selected university.",
)
def pt_fasilitas(id_pt: PTIdParam):
    return as_json(api_client.get_with_keyword("pt/sarpras-file-name", id_pt))


@router.get(
    "/pt/logo/{id_pt}/",
    summary="Get university logo",
    description="Return the logo image of the selected university.",
)
def pt_logo(id_pt: PTIdParam):
    img_data = api_client.get_with_keyword("pt/logo", id_pt)
    if isinstance(img_data, (bytes, bytearray)):
        return Response(content=img_data, media_type="image/png")
    return as_json(img_data)


ENDPOINT_GROUP = {
    "id": "pt",
    "label": "Universities (PT)",
    "description": "Endpoints for university detail, metrics, and assets.",
    "endpoints": [
        {"method": "GET", "path": "/api/pt/detail/{id_pt}/", "summary": "Get university detail"},
        {"method": "GET", "path": "/api/pt/prodi/{id_pt}/{id_thsmt}", "summary": "Get university study programs by semester"},
        {"method": "GET", "path": "/api/pt/rasio/{id_pt}/", "summary": "Get lecturer-student ratio by university"},
        {"method": "GET", "path": "/api/pt/mahasiswa/{id_pt}/", "summary": "Get university student metrics"},
        {"method": "GET", "path": "/api/pt/waktu-studi/{id_pt}/", "summary": "Get average study duration by university"},
        {"method": "GET", "path": "/api/pt/riwayat/{id_pt}/", "summary": "Get university name history"},
        {"method": "GET", "path": "/api/pt/biaya-kuliah/{id_pt}/", "summary": "Get tuition range by university"},
        {"method": "GET", "path": "/api/pt/fasilitas/{id_pt}/", "summary": "Get university facilities metadata"},
        {"method": "GET", "path": "/api/pt/logo/{id_pt}/", "summary": "Get university logo"},
    ],
}
