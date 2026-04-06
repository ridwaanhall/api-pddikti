from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["prodi-bidang-ilmu"])


@router.get(
    "/prodi-bidang-ilmu/agama/",
    summary="Get study programs in religion field",
    description="Return study programs classified under religion-related disciplines.",
)
def prodi_bidang_ilmu_agama():
    return as_json(api_client.get("prodi/bidang-ilmu/Agama"))


@router.get(
    "/prodi-bidang-ilmu/ekonomi/",
    summary="Get study programs in economics field",
    description="Return study programs classified under economics-related disciplines.",
)
def prodi_bidang_ilmu_ekonomi():
    return as_json(api_client.get("prodi/bidang-ilmu/Ekonomi"))


@router.get(
    "/prodi-bidang-ilmu/humaniora/",
    summary="Get study programs in humanities field",
    description="Return study programs classified under humanities-related disciplines.",
)
def prodi_bidang_ilmu_humaniora():
    return as_json(api_client.get("prodi/bidang-ilmu/Humaniora"))


@router.get(
    "/prodi-bidang-ilmu/kesehatan/",
    summary="Get study programs in health field",
    description="Return study programs classified under health-related disciplines.",
)
def prodi_bidang_ilmu_kesehatan():
    return as_json(api_client.get("prodi/bidang-ilmu/Kesehatan"))


@router.get(
    "/prodi-bidang-ilmu/mipa/",
    summary="Get study programs in science field",
    description="Return study programs classified under science and mathematics disciplines.",
)
def prodi_bidang_ilmu_mipa():
    return as_json(api_client.get("prodi/bidang-ilmu/MIPA"))


@router.get(
    "/prodi-bidang-ilmu/pendidikan/",
    summary="Get study programs in education field",
    description="Return study programs classified under education-related disciplines.",
)
def prodi_bidang_ilmu_pendidikan():
    return as_json(api_client.get("prodi/bidang-ilmu/Pendidikan"))


@router.get(
    "/prodi-bidang-ilmu/pertanian/",
    summary="Get study programs in agriculture field",
    description="Return study programs classified under agriculture-related disciplines.",
)
def prodi_bidang_ilmu_pertanian():
    return as_json(api_client.get("prodi/bidang-ilmu/Pertanian"))


@router.get(
    "/prodi-bidang-ilmu/seni/",
    summary="Get study programs in arts field",
    description="Return study programs classified under arts-related disciplines.",
)
def prodi_bidang_ilmu_seni():
    return as_json(api_client.get("prodi/bidang-ilmu/Seni"))


@router.get(
    "/prodi-bidang-ilmu/sosial/",
    summary="Get study programs in social field",
    description="Return study programs classified under social sciences disciplines.",
)
def prodi_bidang_ilmu_sosial():
    return as_json(api_client.get("prodi/bidang-ilmu/Sosial"))


@router.get(
    "/prodi-bidang-ilmu/teknik/",
    summary="Get study programs in engineering field",
    description="Return study programs classified under engineering-related disciplines.",
)
def prodi_bidang_ilmu_teknik():
    return as_json(api_client.get("prodi/bidang-ilmu/Teknik"))


ENDPOINT_GROUP = {
    "id": "prodi-bidang-ilmu",
    "label": "Study Programs by Field",
    "description": "Grouped study program endpoints by major discipline.",
    "endpoints": [
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/agama/", "summary": "Get study programs in religion field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/ekonomi/", "summary": "Get study programs in economics field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/humaniora/", "summary": "Get study programs in humanities field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/kesehatan/", "summary": "Get study programs in health field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/mipa/", "summary": "Get study programs in science field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/pendidikan/", "summary": "Get study programs in education field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/pertanian/", "summary": "Get study programs in agriculture field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/seni/", "summary": "Get study programs in arts field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/sosial/", "summary": "Get study programs in social field"},
        {"method": "GET", "path": "/api/prodi-bidang-ilmu/teknik/", "summary": "Get study programs in engineering field"},
    ],
}
