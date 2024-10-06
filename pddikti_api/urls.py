from django.urls import path
from . import views

urlpatterns = [
    # api overview
    path('', views.api_overview, name='api-overview'),
    
    # search
    path('search/all/<str:keyword>/', views.SearchAll.as_view(), name='search-all'),
    path('search/pt/<str:keyword>/', views.SearchPT.as_view(), name='search-pt'),
    path('search/prodi/<str:keyword>/', views.SearchProdi.as_view(), name='search-prodi'),
    path('search/dosen/<str:keyword>/', views.SearchDosen.as_view(), name='search-dosen'),
    path('search/mhs/<str:keyword>/', views.SearchMahasiswa.as_view(), name='search-mahasiswa'),
    
    # pt
    path('pt/detail/<str:id>/', views.PTDetail.as_view(), name='pt-detail'),
    path('pt/prodi/<str:id>/<str:id_thsmt>', views.PTProdi.as_view(), name='pt-prodi'),
]
