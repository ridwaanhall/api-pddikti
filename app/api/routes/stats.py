from fastapi import APIRouter

from app.api.common import api_client, as_json


router = APIRouter(tags=["statistics"])


@router.get(
    "/stats/mhs-count/",
    summary="Get total student count",
    description="Return aggregate count of all students in the dataset.",
)
def mhs_count():
    return as_json(api_client.get("mahasiswa/count"))


@router.get(
    "/stats/mhs-count-active/",
    summary="Get active student count",
    description="Return aggregate count of active students.",
)
def mhs_count_active():
    return as_json(api_client.get("mahasiswa/count-active"))


@router.get(
    "/stats/mhs-count-gender/",
    summary="Get student count by gender",
    description="Return student distribution grouped by gender.",
)
def mhs_count_gender():
    return as_json(api_client.get("visualisasi/mahasiswa-jenis-kelamin"))


@router.get(
    "/stats/mhs-count-bidang-ilmu/",
    summary="Get student count by field",
    description="Return student distribution grouped by scientific field.",
)
def mhs_count_bidang_ilmu():
    return as_json(api_client.get("visualisasi/mahasiswa-bidang"))


@router.get(
    "/stats/mhs-count-status/",
    summary="Get student count by status",
    description="Return student distribution grouped by academic status.",
)
def mhs_count_status():
    return as_json(api_client.get("visualisasi/mahasiswa-status"))


@router.get(
    "/stats/mhs-count-jenjang/",
    summary="Get student count by degree level",
    description="Return student distribution grouped by degree level.",
)
def mhs_count_jenjang():
    return as_json(api_client.get("visualisasi/mahasiswa-jenjang"))


@router.get(
    "/stats/mhs-count-kelompok-lembaga/",
    summary="Get student count by institution group",
    description="Return student distribution grouped by institution category.",
)
def mhs_count_kelompok_lembaga():
    return as_json(api_client.get("visualisasi/mahasiswa-kelompok-lembaga"))


@router.get(
    "/stats/dosen-count/",
    summary="Get total lecturer count",
    description="Return aggregate count of lecturers in the dataset.",
)
def dosen_count():
    return as_json(api_client.get("dosen/count"))


@router.get(
    "/stats/dosen-count-active/",
    summary="Get active lecturer count",
    description="Return aggregate count of active lecturers.",
)
def dosen_count_active():
    return as_json(api_client.get("dosen/count-active"))


@router.get(
    "/stats/dosen-count-gender/",
    summary="Get lecturer count by gender",
    description="Return lecturer distribution grouped by gender.",
)
def dosen_count_gender():
    return as_json(api_client.get("visualisasi/dosen-jenis-kelamin"))


@router.get(
    "/stats/dosen-count-bidang/",
    summary="Get lecturer count by field",
    description="Return lecturer distribution grouped by scientific field.",
)
def dosen_count_bidang():
    return as_json(api_client.get("visualisasi/dosen-bidang"))


@router.get(
    "/stats/dosen-count-keaktifan/",
    summary="Get lecturer count by activity",
    description="Return lecturer distribution grouped by activity status.",
)
def dosen_count_keaktifan():
    return as_json(api_client.get("visualisasi/dosen-keaktifan"))


@router.get(
    "/stats/dosen-count-jenjang/",
    summary="Get lecturer count by degree",
    description="Return lecturer distribution grouped by degree level.",
)
def dosen_count_jenjang():
    return as_json(api_client.get("visualisasi/dosen-jenjang"))


@router.get(
    "/stats/dosen-count-ikatan/",
    summary="Get lecturer count by affiliation",
    description="Return lecturer distribution grouped by employment affiliation.",
)
def dosen_count_ikatan():
    return as_json(api_client.get("visualisasi/dosen-ikatan"))


@router.get(
    "/stats/pt-count/",
    summary="Get total university count",
    description="Return aggregate count of universities.",
)
def pt_count():
    return as_json(api_client.get("pt/count"))


@router.get(
    "/stats/pt-count-province/",
    summary="Get university count by province",
    description="Return university distribution grouped by province.",
)
def pt_province_count():
    return as_json(api_client.get("visualisasi/pt-provinsi"))


@router.get(
    "/stats/pt-count-kelompok-pembina/",
    summary="Get university count by supervising group",
    description="Return university distribution grouped by supervising institution.",
)
def pt_kelompok_pembina_count():
    return as_json(api_client.get("visualisasi/pt-kelompok-pembina"))


@router.get(
    "/stats/pt-count-akreditasi/",
    summary="Get university count by accreditation",
    description="Return university distribution grouped by accreditation level.",
)
def pt_akreditasi_count():
    return as_json(api_client.get("visualisasi/pt-akreditasi"))


@router.get(
    "/stats/pt-count-bentuk-pt/",
    summary="Get university count by institution type",
    description="Return university distribution grouped by institution type.",
)
def pt_bentuk_perguruan_tinggi_count():
    return as_json(api_client.get("visualisasi/pt-bentuk"))


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


@router.get(
    "/stats/prodi-count-kelompok-pembina/",
    summary="Get study program count by supervising group",
    description="Return study program distribution grouped by supervising institution.",
)
def prodi_kelompok_pembina_count():
    return as_json(api_client.get("visualisasi/prodi-kelompok-pembina"))


@router.get(
    "/stats/prodi-count-bidang-ilmu/",
    summary="Get study program count by field",
    description="Return study program distribution grouped by scientific field.",
)
def prodi_bidang_ilmu_count():
    return as_json(api_client.get("visualisasi/prodi-bidang-ilmu"))


@router.get(
    "/stats/prodi-count-akreditasi/",
    summary="Get study program count by accreditation",
    description="Return study program distribution grouped by accreditation level.",
)
def prodi_akreditasi_count():
    return as_json(api_client.get("visualisasi/prodi-akreditasi"))


@router.get(
    "/stats/prodi-count-jenjang/",
    summary="Get study program count by degree level",
    description="Return study program distribution grouped by degree level.",
)
def prodi_jenjang_count():
    return as_json(api_client.get("visualisasi/prodi-jenjang"))


ENDPOINT_GROUP = {
    "id": "statistics",
    "label": "Statistics",
    "description": "Aggregate counts and visualized distribution metrics.",
    "endpoints": [
        {"method": "GET", "path": "/api/stats/mhs-count/", "summary": "Get total student count"},
        {"method": "GET", "path": "/api/stats/mhs-count-active/", "summary": "Get active student count"},
        {"method": "GET", "path": "/api/stats/mhs-count-gender/", "summary": "Get student count by gender"},
        {"method": "GET", "path": "/api/stats/mhs-count-bidang-ilmu/", "summary": "Get student count by field"},
        {"method": "GET", "path": "/api/stats/mhs-count-status/", "summary": "Get student count by status"},
        {"method": "GET", "path": "/api/stats/mhs-count-jenjang/", "summary": "Get student count by degree level"},
        {"method": "GET", "path": "/api/stats/mhs-count-kelompok-lembaga/", "summary": "Get student count by institution group"},
        {"method": "GET", "path": "/api/stats/dosen-count/", "summary": "Get total lecturer count"},
        {"method": "GET", "path": "/api/stats/dosen-count-active/", "summary": "Get active lecturer count"},
        {"method": "GET", "path": "/api/stats/dosen-count-gender/", "summary": "Get lecturer count by gender"},
        {"method": "GET", "path": "/api/stats/dosen-count-bidang/", "summary": "Get lecturer count by field"},
        {"method": "GET", "path": "/api/stats/dosen-count-keaktifan/", "summary": "Get lecturer count by activity"},
        {"method": "GET", "path": "/api/stats/dosen-count-jenjang/", "summary": "Get lecturer count by degree"},
        {"method": "GET", "path": "/api/stats/dosen-count-ikatan/", "summary": "Get lecturer count by affiliation"},
        {"method": "GET", "path": "/api/stats/pt-count/", "summary": "Get total university count"},
        {"method": "GET", "path": "/api/stats/pt-count-province/", "summary": "Get university count by province"},
        {"method": "GET", "path": "/api/stats/pt-count-kelompok-pembina/", "summary": "Get university count by supervising group"},
        {"method": "GET", "path": "/api/stats/pt-count-akreditasi/", "summary": "Get university count by accreditation"},
        {"method": "GET", "path": "/api/stats/pt-count-bentuk-pt/", "summary": "Get university count by institution type"},
        {"method": "GET", "path": "/api/stats/prodi-count/", "summary": "Get total study program count"},
        {"method": "GET", "path": "/api/stats/prodi-count-bidang-ilmu-terbanyak/", "summary": "Get most common study program field"},
        {"method": "GET", "path": "/api/stats/prodi-count-kelompok-pembina/", "summary": "Get study program count by supervising group"},
        {"method": "GET", "path": "/api/stats/prodi-count-bidang-ilmu/", "summary": "Get study program count by field"},
        {"method": "GET", "path": "/api/stats/prodi-count-akreditasi/", "summary": "Get study program count by accreditation"},
        {"method": "GET", "path": "/api/stats/prodi-count-jenjang/", "summary": "Get study program count by degree level"},
    ],
}
