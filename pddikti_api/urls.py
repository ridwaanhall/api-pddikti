from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('search/all/<str:keyword>/', views.SearchAll.as_view(), name='search-all'),
    path('search/pt/<str:keyword>/', views.SearchPT.as_view(), name='search-pt'),
    path('search/prodi/<str:keyword>/', views.SearchProdi.as_view(), name='search-prodi'),
    path('search/dosen/<str:keyword>/', views.SearchDosen.as_view(), name='search-dosen'),
    path('search/mhs/<str:keyword>/', views.SearchMahasiswa.as_view(), name='search-mahasiswa'),
]
