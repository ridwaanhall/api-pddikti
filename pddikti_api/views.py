from django.conf import settings
from django.http import HttpResponse
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

@api_view(['GET'])
def api_overview(_):
    return Response({
        "message": "Welcome to the PDDIKTI API!",
        "endpoints": {
            "Search Endpoints": {
                "Search All": {
                    "url": "/search/all/<str:keyword>/",
                    "method": "GET",
                    "description": "Search across all categories using the provided keyword.",
                    "parameters": {
                        "keyword": "string: The keyword to search for."
                    }
                },
                "Search PT": {
                    "url": "/search/pt/<str:keyword>/",
                    "method": "GET",
                    "description": "Search for PT (Perguruan Tinggi) using the provided keyword.",
                    "parameters": {
                        "keyword": "string: The keyword to search for."
                    }
                },
                "Search Prodi": {
                    "url": "/search/prodi/<str:keyword>/",
                    "method": "GET",
                    "description": "Search for Prodi (Program Studi) using the provided keyword.",
                    "parameters": {
                        "keyword": "string: The keyword to search for."
                    }
                },
                "Search Dosen": {
                    "url": "/search/dosen/<str:keyword>/",
                    "method": "GET",
                    "description": "Search for Dosen (Lecturer) using the provided keyword.",
                    "parameters": {
                        "keyword": "string: The keyword to search for."
                    }
                },
                "Search Mahasiswa": {
                    "url": "/search/mhs/<str:keyword>/",
                    "method": "GET",
                    "description": "Search for Mahasiswa (Student) using the provided keyword.",
                    "parameters": {
                        "keyword": "string: The keyword to search for."
                    }
                }
            },
            "PT Endpoints": {
                "PT Detail": {
                    "url": "/pt/detail/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get details of a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Prodi": {
                    "url": "/pt/prodi/<str:id_pt>/<str:id_thsmt>/",
                    "method": "GET",
                    "description": "Get Prodi details of a specific PT for a given semester.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT.",
                        "id_thsmt": "string: The ID of the semester."
                    }
                },
                "PT Rasio": {
                    "url": "/pt/rasio/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the ratio of lecturers to students for a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Mahasiswa": {
                    "url": "/pt/mahasiswa/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the mean number of graduates and new students for a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Waktu Studi": {
                    "url": "/pt/waktu-studi/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the mean study duration for a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Riwayat": {
                    "url": "/pt/riwayat/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the history of a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Biaya Kuliah": {
                    "url": "/pt/biaya-kuliah/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the tuition fees for a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Fasilitas": {
                    "url": "/pt/fasilitas/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the facilities of a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                },
                "PT Logo": {
                    "url": "/pt/logo/<str:id_pt>/",
                    "method": "GET",
                    "description": "Get the logo of a specific PT.",
                    "parameters": {
                        "id_pt": "string: The ID of the PT."
                    }
                }
            },
            "Prodi Endpoints": {
                "Prodi Detail": {
                    "url": "/prodi/detail/<str:id_prodi>/",
                    "method": "GET",
                    "description": "Get details of a specific Prodi.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi."
                    }
                },
                "Prodi Desc": {
                    "url": "/prodi/desc/<str:id_prodi>/",
                    "method": "GET",
                    "description": "Get the description of a specific Prodi.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi."
                    }
                },
                "Prodi Num Students Lecturers": {
                    "url": "/prodi/num-students-lecturers/<str:id_prodi>/",
                    "method": "GET",
                    "description": "Get the number of students and lecturers for a specific Prodi.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi."
                    }
                },
                "Prodi Riwayat": {
                    "url": "/prodi/riwayat/<str:id_prodi>/",
                    "method": "GET",
                    "description": "Get the history of a specific Prodi.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi."
                    }
                },
                "Prodi Biaya Kuliah": {
                    "url": "/prodi/biaya-kuliah/<str:id_prodi>/",
                    "method": "GET",
                    "description": "Get the tuition fees for a specific Prodi.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi."
                    }
                },
                "Prodi Dosen Homebase": {
                    "url": "/prodi/dosen-homebase/<str:id_prodi>/<str:id_thsmt>/",
                    "method": "GET",
                    "description": "Get the homebase lecturers for a specific Prodi for a given semester.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi.",
                        "id_thsmt": "string: The ID of the semester."
                    }
                },
                "Prodi Dosen Penghitung Ratio": {
                    "url": "/prodi/dosen-penghitung-ratio/<str:id_prodi>/<str:id_thsmt>/",
                    "method": "GET",
                    "description": "Get the lecturers who count towards the ratio for a specific Prodi for a given semester.",
                    "parameters": {
                        "id_prodi": "string: The ID of the Prodi.",
                        "id_thsmt": "string: The ID of the semester."
                    }
                }
            },
            "Dosen Endpoints": {
                "Dosen Profile": {
                    "url": "/dosen/profile/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the profile of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Study History": {
                    "url": "/dosen/study-history/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the study history of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Teaching History": {
                    "url": "/dosen/teaching-history/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the teaching history of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Portofolio Penelitian": {
                    "url": "/dosen/portofolio/penelitian/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the research portfolio of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Portofolio Pengabdian": {
                    "url": "/dosen/portofolio/pengabdian/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the community service portfolio of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Portofolio Karya": {
                    "url": "/dosen/portofolio/karya/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the works portfolio of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                },
                "Dosen Portofolio Paten": {
                    "url": "/dosen/portofolio/paten/<str:id_dosen>/",
                    "method": "GET",
                    "description": "Get the patents portfolio of a specific Dosen.",
                    "parameters": {
                        "id_dosen": "string: The ID of the Dosen."
                    }
                }
            }
        }
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