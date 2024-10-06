from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

BASE_URL = "https://pddikti.kemdikbud.go.id/api/pencarian"

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

@api_view(['GET'])
def api_overview(_):
    return Response({
        "message": "Welcome to the PDDIKTI API!"
    })

class SearchAll(APIView):
    def get(self, _, keyword):
        data = make_api_request('all', keyword)
        return Response(data)

class SearchPT(APIView):
    def get(self, _, keyword):
        data = make_api_request('pt', keyword)
        return Response(data)

class SearchProdi(APIView):
    def get(self, _, keyword):
        data = make_api_request('prodi', keyword)
        return Response(data)

class SearchDosen(APIView):
    def get(self, _, keyword):
        data = make_api_request('dosen', keyword)
        return Response(data)

class SearchMahasiswa(APIView):
    def get(self, _, keyword):
        data = make_api_request('mhs', keyword)
        return Response(data)