import json
from urllib.parse import unquote
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

BASE_URL = settings.PDDIKTI_API_URL

def make_api_request(endpoint, keyword):
    decoded_keyword = unquote(keyword)
    api_url = f"{BASE_URL}/{endpoint}/{decoded_keyword}"
    headers = {
        'Host': settings.HOST_KEY,
        'Origin': settings.ORIGIN_KEY,
        'Referer': settings.REFERER_KEY,
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': 'Connection error occurred', 'details': str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': 'Request timed out', 'details': str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        return {'error': 'An error occurred', 'details': str(req_err)}

def make_api_request_2(endpoint, id, id_thsmt):
    decoded_keyword = unquote(id)
    api_url = f"{BASE_URL}/{endpoint}/{decoded_keyword}/{id_thsmt}"
    headers = {
        'Host': settings.HOST_KEY,
        'Origin': settings.ORIGIN_KEY,
        'Referer': settings.REFERER_KEY,
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': 'Connection error occurred', 'details': str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': 'Request timed out', 'details': str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        return {'error': 'An error occurred', 'details': str(req_err)}

def make_api_request_3(endpoint, id, id_thsmt):
    decoded_keyword = unquote(id)
    api_url = f"{BASE_URL}/{endpoint}/{decoded_keyword}?semester={id_thsmt}"
    headers = {
        'Host': settings.HOST_KEY,
        'Origin': settings.ORIGIN_KEY,
        'Referer': settings.REFERER_KEY,
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': 'Connection error occurred', 'details': str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': 'Request timed out', 'details': str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        return {'error': 'An error occurred', 'details': str(req_err)}

def make_api_request_no_keyword(endpoint):
    api_url = f"{BASE_URL}/{endpoint}"
    headers = {
        'Host': settings.HOST_KEY,
        'Origin': settings.ORIGIN_KEY,
        'Referer': settings.REFERER_KEY,
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': 'Connection error occurred', 'details': str(conn_err)}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': 'Request timed out', 'details': str(timeout_err)}
    except requests.exceptions.RequestException as req_err:
        return {'error': 'An error occurred', 'details': str(req_err)}

def make_api_request_img(endpoint, id):
    decoded_keyword = unquote(id)
    api_url = f"{BASE_URL}/{endpoint}/{decoded_keyword}"
    headers = {
        'Host': settings.HOST_KEY,
        'Origin': settings.ORIGIN_KEY,
        'Referer': settings.REFERER_KEY,
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as http_err:
        return None
    except requests.exceptions.ConnectionError as conn_err:
        return None
    except requests.exceptions.Timeout as timeout_err:
        return None
    except requests.exceptions.RequestException as req_err:
        return None

class APIOverview(APIView):
    def get(self, _):
        with open('api_overview.json', 'r') as file:
            data = json.load(file)
        return Response(data)

# SearchAll, SearchPT, SearchProdi, SearchDosen, and SearchMahasiswa classes are API views that handle GET requests.
class SearchAll(APIView):
    def get(self, _, keyword):
        data = make_api_request('pencarian/all', keyword)
        return Response(data)

class SearchPT(APIView):
    def get(self, _, keyword):
        data = make_api_request('pencarian/pt', keyword)
        return Response(data)

class SearchProdi(APIView):
    def get(self, _, keyword):
        data = make_api_request('pencarian/prodi', keyword)
        return Response(data)

class SearchDosen(APIView):
    def get(self, _, keyword):
        data = make_api_request('pencarian/dosen', keyword)
        return Response(data)

class SearchMahasiswa(APIView):
    def get(self, _, keyword):
        data = make_api_request('pencarian/mhs', keyword)
        return Response(data)
    
# PT
class PTDetail(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/detail', id_pt)
        return Response(data)

class PTProdi(APIView):
    def get(self, _, id_pt, id_thsmt):
        data = make_api_request_2('pt/prodi', id_pt, id_thsmt)
        return Response(data)
    
class PTRasioDosenMahasiswa(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/rasio', id_pt)
        return Response(data)
    
class PTMeanLulusMaba(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/mahasiswa', id_pt)
        return Response(data)
    
class PTMeanMasaStudi(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/waktu-studi', id_pt)
        return Response(data)
    
class PTRiwayat(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/name-histories', id_pt)
        return Response(data)
    
class PTBiayaKuliah(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/cost-range', id_pt)
        return Response(data)
    
class PTFasilitas(APIView):
    def get(self, _, id_pt):
        data = make_api_request('pt/sarpras-file-name', id_pt)
        return Response(data)
    
class PTLogo(APIView):
    def get(self, request, id_pt):
        img_data = make_api_request_img('pt/logo', id_pt)
        if img_data:
            return HttpResponse(img_data, content_type="image/png")
        else:
            return HttpResponse(status=404)
        
# prodi
class ProdiDetail(APIView):
    def get(self, _, id_prodi):
        data = make_api_request('prodi/detail', id_prodi)
        return Response(data)
    
class ProdiDesc(APIView):
    def get(self, _, id_prodi):
        data = make_api_request('prodi/desc', id_prodi)
        return Response(data)
    
class ProdiJumlahMHSDosen(APIView):
    def get(self, _, id_prodi):
        data = make_api_request('prodi/num-students-lecturers', id_prodi)
        return Response(data)
    
class ProdiRiwayat(APIView):
    def get(self, _, id_prodi):
        data = make_api_request('prodi/name-histories', id_prodi)
        return Response(data)
    
class ProdiBiayaKuliah(APIView):
    def get(self, _, id_prodi):
        data = make_api_request('prodi/cost-range', id_prodi)
        return Response(data)
    
class ProdiDosenHomebase(APIView):
    def get(self, _, id_prodi, id_thsmt):
        data = make_api_request_3('dosen/homebase', id_prodi, id_thsmt)
        return Response(data)
    
class ProdiDosenPenghitungRatio(APIView):
    def get(self, _, id_prodi, id_thsmt):
        data = make_api_request_3('dosen/penghitung-ratio', id_prodi, id_thsmt)
        return Response(data)

# dosen
class DosenProfile(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/profile', id_dosen)
        return Response(data)
    
class DosenRiwayatPendidikan(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/study-history', id_dosen)
        return Response(data)
    
class DosenRiwayatMengajar(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/teaching-history', id_dosen)
        return Response(data)
    
class DosenPortofolioPenelitian(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/portofolio/penelitian', id_dosen)
        return Response(data)
    
class DosenPortofolioPengabdian(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/portofolio/pengabdian', id_dosen)
        return Response(data)
    
class DosenPortofolioKarya(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/portofolio/karya', id_dosen)
        return Response(data)

class DosenPortofolioPaten(APIView):
    def get(self, _, id_dosen):
        data = make_api_request('dosen/portofolio/paten', id_dosen)
        return Response(data)
    
# mahasiswa
class MhsDetail(APIView):
    def get(self, _, id_mhs):
        data = make_api_request('detail/mhs', id_mhs)
        return Response(data)

# statistic mhs
class MhsCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('mahasiswa/count')
        return Response(data)

class MhsCountActive(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('mahasiswa/count-active')
        return Response(data)
    
class MhsCountGender(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/mahasiswa-jenis-kelamin')
        
class MhsCountBidangIlmu(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/mahasiswa-bidang')
        return Response(data)
    
class MhsCountStatus(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/mahasiswa-status')
        return Response(data)
    
class MhsCountJenjang(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/mahasiswa-jenjang')
        return Response(data)
    
class MhsCountKelompokLembaga(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/mahasiswa-kelompok-lembaga')
        return Response(data)
    
# statistic dosen
class DosenCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('dosen/count')
        return Response(data)
    
class DosenCountActive(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('dosen/count-active')
        return Response(data)

class DosenCountGender(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/dosen-jenis-kelamin')
        return Response(data)
    
class DosenCountBidang(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/dosen-bidang')
        return Response(data)
    
class DosenCountKeaktifan(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/dosen-keaktifan')
        return Response(data)
    
class DosenCountJenjang(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/dosen-jenjang')
        return Response(data)
    
class DosenCountIkatan(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/dosen-ikatan')
        return Response(data)

# pt
class PTCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('pt/count')
        return Response(data)
    
class PTProvinceCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/pt-provinsi')
        return Response(data)
    
class PTKelompokPembinaCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/pt-kelompok-pembina')
        return Response(data)
    
class PTAkreditasiCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/pt-akreditasi')
        return Response(data)
    
class PTBentukPerguruanTinggiCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/pt-bentuk')
        return Response(data)
    
# prodi
class ProdiCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/count')
        return Response(data)
    
class ProdiBidangIlmuTerbanyakCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu')
        return Response(data)
    
class ProdiKelompokPembinaCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/prodi-kelompok-pembina')
        return Response(data)
    
class ProdiBidangIlmuCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/prodi-bidang-ilmu')
        return Response(data)
    
class ProdiAkreditasiCOunt(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/prodi-akreditasi')
        return Response(data)
    
class ProdiJenjangCount(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('visualisasi/prodi-jenjang')
        return Response(data)

# prodi bidang ilmu
class ProdiBidangIlmuAgama(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Agama')
        return Response(data)
    
class ProdiBidangIlmuEkonomi(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Ekonomi')
        return Response(data)
    
class ProdiBidangIlmuHumaniora(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Humaniora')
        return Response(data)
    
class ProdiBidangIlmukesehatan(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Kesehatan')
        return Response(data)
    
class ProdiBidangIlmuMIPA(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/MIPA')
        return Response(data)

class ProdiBidangIlmuPendidikan(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Pendidikan')
        return Response(data)

class ProdiBidangIlmuPertanian(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Pertanian')
        return Response(data)

class ProdiBidangIlmuSeni(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Seni')
        return Response(data)

class ProdiBidangIlmuSosial(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Sosial')
        return Response(data)

class ProdiBidangIlmuTeknik(APIView):
    def get(self, _):
        data = make_api_request_no_keyword('prodi/bidang-ilmu/Teknik')
        return Response(data)