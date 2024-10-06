from django.conf import settings
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
        response = requests.get(api_url, headers=headers, timeout=10)
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
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

@api_view(['GET'])
def api_overview(_):
    return Response({
        "message": "Welcome to the PDDIKTI API!"
    })

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
    def get(self, _, id):
        data = make_api_request('pt/detail', id)
        return Response(data)

class PTProdi(APIView):
    def get(self, _, id, id_thsmt):
        data = make_api_request_2('pt/prodi', id, id_thsmt)
        return Response(data)