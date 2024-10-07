import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

BASE_URL = settings.PDDIKTI_API_URL

def make_api_request(endpoint, keyword):
    api_url = f"{BASE_URL}/{endpoint}/{keyword}"
    headers = {
        'x-api-key': settings.API_KEY
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
def make_api_request_2(endpoint, id, id_thsmt):
    api_url = f"{BASE_URL}/{endpoint}/{id}/{id_thsmt}"
    headers = {
        'x-api-key': settings.API_KEY
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
def make_api_request_3(endpoint, id, id_thsmt):
    api_url = f"{BASE_URL}/{endpoint}/{id}?semester={id_thsmt}"
    headers = {
        'x-api-key': settings.API_KEY
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
def make_api_request_img(endpoint, id):
    api_url = f"{BASE_URL}/{endpoint}/{id}"
    headers = {
        'x-api-key': settings.API_KEY
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
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