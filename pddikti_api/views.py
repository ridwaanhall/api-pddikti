from typing import Any
from urllib.parse import unquote

import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

BASE_URL = settings.RIDWAANHALL_MAIN_API
API_AVAILABILITY = settings.API_AVAILABILITY


class APIClient:
    """
    A class to handle making requests to the RIDWAANHALL API.
    """

    def __init__(self):
        self.headers = {
            settings.RIDWAANHALL_API_X: settings.RIDWAANHALL_API_KEY,
            settings.RIDWAANHALL_X: settings.RIDWAANHALL_KEY,
            settings.RIDWAANHALL_HASH_X: settings.RIDWAANHALL_HASH_KEY,
        }
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handles the response from the API.

        Args:
            response (requests.Response): The response object from the API.

        Returns:
             Any: The JSON response data or None for images.
        """
        try:
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            if "image" in response.headers.get("Content-Type", ""):
                return response.content  # Return raw content for images
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {
                "code": response.status_code,
                "error": "HTTP error occurred",
                "message": response.json(),
            }
        except requests.exceptions.ConnectionError as conn_err:
            return {
                "code": response.status_code,
                "error": "Connection error occurred",
                "message": response.json(),
            }
        except requests.exceptions.Timeout as timeout_err:
            return {
                "code": response.status_code,
                "error": "Request timed out",
                "message": response.json(),
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "code": response.status_code,
                "error": "An error occurred",
                "message": response.json(),
            }

    def _make_request(self, url: str) -> Any:
        """
        Makes an API request with error handling

        Args:
            url (str): The complete URL for the request.

        Returns:
            Any: The data received from the API or error object.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            print(url)
            print(self.headers)

            return {
                "error": "An unexpected error occurred", 
                "message": "Please try again later or contact the administrator.",
            }

    def get(self, endpoint: str, **kwargs: str) -> Any:
        """
        Makes a GET request to the RIDWAANHALL API.

        Args:
            endpoint (str): The API endpoint.
            **kwargs (str): Optional parameters for the URL.

        Returns:
           Any: The API response data or None if there was an error.
        """
        url = f"{BASE_URL}/{endpoint}"
        if kwargs:
            params = "&".join([f"{k}={unquote(v)}" for k, v in kwargs.items()])
            url = f"{url}?{params}"

        return self._make_request(url)

    def get_with_keyword(self, endpoint: str, keyword: str) -> Any:
        """
        Makes a GET request with a keyword in the URL.

        Args:
            endpoint (str): The API endpoint.
            keyword (str): The keyword for the request.

        Returns:
             Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(keyword)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}"
        return self._make_request(url)

    def get_with_id_and_semester(self, endpoint: str, id: str, id_thsmt: str) -> Any:
        """
        Makes a GET request with ID and semester parameters

        Args:
             endpoint (str): The API endpoint.
             id (str): The ID for the request.
             id_thsmt (str): The semester ID.

        Returns:
            Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(id)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}/{id_thsmt}"
        return self._make_request(url)

    def get_with_id_and_param_semester(self, endpoint: str, id: str, id_thsmt: str) -> Any:
        """
        Makes a GET request with ID and semester parameters

        Args:
             endpoint (str): The API endpoint.
             id (str): The ID for the request.
             id_thsmt (str): The semester ID.

        Returns:
            Any: The API response data or None if there was an error.
        """
        decoded_keyword = unquote(id)
        url = f"{BASE_URL}/{endpoint}/{decoded_keyword}?semester={id_thsmt}"
        return self._make_request(url)


class BaseAPIView(APIView):
    """
    Base class for API views, providing common functionality.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()

    def handle_api_response(self, data: Any) -> Response:
        """
        Handles the API response and returns a Response object

        Args:
             data (Any): The data received from the API.

        Returns:
            Response: The API response for client
        """
        return Response(data)


# API Views
class APIOverview(BaseAPIView):
    def get(self, _):
        meta = {
            "base_url": "https://api-pddikti.ridwaanhall.com/",
            "version": {
                "current": settings.API_VERSION,
                "minimum_supported": settings.API_VERSION,
            },
            "description": (
                "Provides structured access to data from Pangkalan Data Pendidikan Tinggi (PDDikti), "
                "Indonesia’s Higher Education Database"
            ),
            "last_updated": "2025-07-26T18:48:00+07:00",
            "author": "ridwaanhall"
        }
        resources = {
            "api_docs": "https://pddikti-docs.ridwaanhall.com/",
            "api_root": "https://api-pddikti.ridwaanhall.com/",
            "official_website": "https://pddikti.kemdiktisaintek.go.id/"
        }
        features = {
            "documentation": "Comprehensive API guide with endpoints, examples, and usage instructions",
            "status_monitoring": "Real-time performance and availability tracking",
            "traffic_management": "Automated request balancing and throttling for high availability"
        }
        if API_AVAILABILITY:
            status = {
                "status": "Operational",
                "code": "OK_200",
                "severity": "normal",
                "message": "All endpoints are functioning normally."
            }
            notice = {
                "headline": "Service Operational",
                "details": "Traffic levels have normalized and full services are restored.",
                "estimated_resolution": None,
                "support_contact": {
                    "live_chat": "https://ridwaanhall.com/guestbook",
                    "email": "hi@ridwaanhall.com",
                    "form": "https://ridwaanhall.com/contact"
                }
            }
        else:
            status = {
                "status": "Limited Service",
                "code": "TRAFFIC_LIMIT_001",
                "severity": "warning",
                "message": "Some endpoints are temporarily unavailable due to high traffic"
            }
            notice = {
                "headline": "High Traffic Alert",
                "details": "To maintain stability, some services are temporarily limited.",
                "estimated_resolution": "Expected recovery as traffic normalizes within days or weeks",
                "blog": "https://ridwaanhall.com/blog/how-usage-monitoring-sustains-mlbb-stats-and-api-pddikti/",
                "support_contact": {
                    "live_chat": "https://ridwaanhall.com/guestbook",
                    "email": "hi@ridwaanhall.com",
                    "form": "https://ridwaanhall.com/contact"
                }
            }
            meta["description"] += ", covering universities, study programs, lecturers, and students."
        data = {
            "meta": meta,
            "resources": resources,
            "features": features,
            "status": status,
            "notice": notice
        }
        return self.handle_api_response(data)


# Search
class SearchAll(BaseAPIView):
    def get(self, _, keyword):
        data = self.api_client.get_with_keyword("pencarian/all", keyword)
        return self.handle_api_response(data)

class SearchPT(BaseAPIView):
    def get(self, _, keyword):
        data = self.api_client.get_with_keyword("pencarian/pt", keyword)
        return self.handle_api_response(data)

class SearchProdi(BaseAPIView):
    def get(self, _, keyword):
        data = self.api_client.get_with_keyword("pencarian/prodi", keyword)
        return self.handle_api_response(data)

class SearchDosen(BaseAPIView):
    def get(self, _, keyword):
        data = self.api_client.get_with_keyword("pencarian/dosen", keyword)
        return self.handle_api_response(data)

class SearchMahasiswa(BaseAPIView):
    def get(self, _, keyword):
        data = self.api_client.get_with_keyword("pencarian/mhs", keyword)
        return self.handle_api_response(data)


# PT
class PTDetail(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/detail", id_pt)
        return self.handle_api_response(data)

class PTProdi(BaseAPIView):
    def get(self, _, id_pt, id_thsmt):
        data = self.api_client.get_with_id_and_semester("pt/prodi", id_pt, id_thsmt)
        return self.handle_api_response(data)

class PTRasioDosenMahasiswa(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/rasio", id_pt)
        return self.handle_api_response(data)

class PTMeanLulusMaba(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/mahasiswa", id_pt)
        return self.handle_api_response(data)

class PTMeanMasaStudi(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/waktu-studi", id_pt)
        return self.handle_api_response(data)

class PTRiwayat(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/name-histories", id_pt)
        return self.handle_api_response(data)

class PTBiayaKuliah(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/cost-range", id_pt)
        return self.handle_api_response(data)

class PTFasilitas(BaseAPIView):
    def get(self, _, id_pt):
        data = self.api_client.get_with_keyword("pt/sarpras-file-name", id_pt)
        return self.handle_api_response(data)

class PTLogo(BaseAPIView):
    def get(self, request, id_pt):
        img_data = self.api_client.get_with_keyword("pt/logo", id_pt)
        if img_data:
            return HttpResponse(img_data, content_type="image/png")
        else:
            return HttpResponse(status=404)


# prodi
class ProdiDetail(BaseAPIView):
    def get(self, _, id_prodi):
        data = self.api_client.get_with_keyword("prodi/detail", id_prodi)
        return self.handle_api_response(data)

class ProdiDesc(BaseAPIView):
    def get(self, _, id_prodi):
        data = self.api_client.get_with_keyword("prodi/desc", id_prodi)
        return self.handle_api_response(data)

class ProdiJumlahMHSDosen(BaseAPIView):
    def get(self, _, id_prodi):
        data = self.api_client.get_with_keyword(
            "prodi/num-students-lecturers", id_prodi
        )
        return self.handle_api_response(data)

class ProdiRiwayat(BaseAPIView):
    def get(self, _, id_prodi):
        data = self.api_client.get_with_keyword("prodi/name-histories", id_prodi)
        return self.handle_api_response(data)

class ProdiBiayaKuliah(BaseAPIView):
    def get(self, _, id_prodi):
        data = self.api_client.get_with_keyword("prodi/cost-range", id_prodi)
        return self.handle_api_response(data)

class ProdiDosenHomebase(BaseAPIView):
    def get(self, _, id_prodi, id_thsmt):
        data = self.api_client.get_with_id_and_param_semester("dosen/homebase", id_prodi, id_thsmt)
        return self.handle_api_response(data)

class ProdiDosenPenghitungRatio(BaseAPIView):
    def get(self, _, id_prodi, id_thsmt):
        data = self.api_client.get_with_id_and_param_semester(
            "dosen/penghitung-ratio", id_prodi, id_thsmt
        )
        return self.handle_api_response(data)


# dosen
class DosenProfile(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/profile", id_dosen)
        return self.handle_api_response(data)

class DosenRiwayatPendidikan(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/study-history", id_dosen)
        return self.handle_api_response(data)

class DosenRiwayatMengajar(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/teaching-history", id_dosen)
        return self.handle_api_response(data)

class DosenPortofolioPenelitian(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/portofolio/penelitian", id_dosen)
        return self.handle_api_response(data)

class DosenPortofolioPengabdian(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/portofolio/pengabdian", id_dosen)
        return self.handle_api_response(data)

class DosenPortofolioKarya(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/portofolio/karya", id_dosen)
        return self.handle_api_response(data)

class DosenPortofolioPaten(BaseAPIView):
    def get(self, _, id_dosen):
        data = self.api_client.get_with_keyword("dosen/portofolio/paten", id_dosen)
        return self.handle_api_response(data)

# mahasiswa
class MhsDetail(BaseAPIView):
    def get(self, _, id_mhs):
        data = self.api_client.get_with_keyword("detail/mhs", id_mhs)
        return self.handle_api_response(data)

# statistic mhs
class MhsCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("mahasiswa/count")
        return self.handle_api_response(data)

class MhsCountActive(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("mahasiswa/count-active")
        return self.handle_api_response(data)

class MhsCountGender(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/mahasiswa-jenis-kelamin")
        return self.handle_api_response(data)

class MhsCountBidangIlmu(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/mahasiswa-bidang")
        return self.handle_api_response(data)

class MhsCountStatus(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/mahasiswa-status")
        return self.handle_api_response(data)

class MhsCountJenjang(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/mahasiswa-jenjang")
        return self.handle_api_response(data)

class MhsCountKelompokLembaga(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/mahasiswa-kelompok-lembaga")
        return self.handle_api_response(data)


# statistic dosen
class DosenCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("dosen/count")
        return self.handle_api_response(data)

class DosenCountActive(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("dosen/count-active")
        return self.handle_api_response(data)

class DosenCountGender(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/dosen-jenis-kelamin")
        return self.handle_api_response(data)

class DosenCountBidang(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/dosen-bidang")
        return self.handle_api_response(data)

class DosenCountKeaktifan(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/dosen-keaktifan")
        return self.handle_api_response(data)

class DosenCountJenjang(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/dosen-jenjang")
        return self.handle_api_response(data)

class DosenCountIkatan(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/dosen-ikatan")
        return self.handle_api_response(data)


# pt
class PTCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("pt/count")
        return self.handle_api_response(data)

class PTProvinceCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/pt-provinsi")
        return self.handle_api_response(data)

class PTKelompokPembinaCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/pt-kelompok-pembina")
        return self.handle_api_response(data)

class PTAkreditasiCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/pt-akreditasi")
        return self.handle_api_response(data)

class PTBentukPerguruanTinggiCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/pt-bentuk")
        return self.handle_api_response(data)


# prodi
class ProdiCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/count")
        return self.handle_api_response(data)

class ProdiBidangIlmuTerbanyakCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu")
        return self.handle_api_response(data)

class ProdiKelompokPembinaCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/prodi-kelompok-pembina")
        return self.handle_api_response(data)

class ProdiBidangIlmuCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/prodi-bidang-ilmu")
        return self.handle_api_response(data)

class ProdiAkreditasiCOunt(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/prodi-akreditasi")
        return self.handle_api_response(data)

class ProdiJenjangCount(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("visualisasi/prodi-jenjang")
        return self.handle_api_response(data)


# prodi bidang ilmu
class ProdiBidangIlmuAgama(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Agama")
        return self.handle_api_response(data)

class ProdiBidangIlmuEkonomi(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Ekonomi")
        return self.handle_api_response(data)

class ProdiBidangIlmuHumaniora(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Humaniora")
        return self.handle_api_response(data)

class ProdiBidangIlmukesehatan(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Kesehatan")
        return self.handle_api_response(data)

class ProdiBidangIlmuMIPA(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/MIPA")
        return self.handle_api_response(data)

class ProdiBidangIlmuPendidikan(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Pendidikan")
        return self.handle_api_response(data)

class ProdiBidangIlmuPertanian(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Pertanian")
        return self.handle_api_response(data)

class ProdiBidangIlmuSeni(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Seni")
        return self.handle_api_response(data)

class ProdiBidangIlmuSosial(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Sosial")
        return self.handle_api_response(data)

class ProdiBidangIlmuTeknik(BaseAPIView):
    def get(self, _):
        data = self.api_client.get("prodi/bidang-ilmu/Teknik")
        return self.handle_api_response(data)
