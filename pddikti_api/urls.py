from django.urls import path
from . import views

urlpatterns = [
    # api overview
    path('', views.APIOverview.as_view(), name='api-overview'),
    
    # search
    path('search/all/<str:keyword>/', views.SearchAll.as_view(), name='search-all'),
    path('search/pt/<str:keyword>/', views.SearchPT.as_view(), name='search-pt'),
    path('search/prodi/<str:keyword>/', views.SearchProdi.as_view(), name='search-prodi'),
    path('search/dosen/<str:keyword>/', views.SearchDosen.as_view(), name='search-dosen'),
    path('search/mhs/<str:keyword>/', views.SearchMahasiswa.as_view(), name='search-mahasiswa'),
    
    # pt
    path('pt/detail/<str:id_pt>/', views.PTDetail.as_view(), name='pt-detail'),
    path('pt/prodi/<str:id_pt>/<str:id_thsmt>', views.PTProdi.as_view(), name='pt-prodi'),
    path('pt/rasio/<str:id_pt>/', views.PTRasioDosenMahasiswa.as_view(), name='pt-rasio'),
    path('pt/mahasiswa/<str:id_pt>/', views.PTMeanLulusMaba.as_view(), name='pt-mahasiswa'),
    path('pt/waktu-studi/<str:id_pt>/', views.PTMeanMasaStudi.as_view(), name='pt-waktu-studi'),
    path('pt/riwayat/<str:id_pt>/', views.PTRiwayat.as_view(), name='pt-riwayat'),
    path('pt/biaya-kuliah/<str:id_pt>/', views.PTBiayaKuliah.as_view(), name='pt-biaya-kuliah'),
    path('pt/fasilitas/<str:id_pt>/', views.PTFasilitas.as_view(), name='pt-fasilitas'),
    path('pt/logo/<str:id_pt>/', views.PTLogo.as_view(), name='pt-logo'),
    
    # prodi
    path('prodi/detail/<str:id_prodi>/', views.ProdiDetail.as_view(), name='prodi-detail'),
    path('prodi/desc/<str:id_prodi>/', views.ProdiDesc.as_view(), name='prodi-desc'),
    path('prodi/num-students-lecturers/<str:id_prodi>/', views.ProdiJumlahMHSDosen.as_view(), name='prodi-num-students-lecturers'),
    path('prodi/riwayat/<str:id_prodi>/', views.ProdiRiwayat.as_view(), name='prodi-riwayat'),
    path('prodi/biaya-kuliah/<str:id_prodi>/', views.ProdiBiayaKuliah.as_view(), name='prodi-biaya-kuliah'),
    path('prodi/dosen-homebase/<str:id_prodi>/<str:id_thsmt>/', views.ProdiDosenHomebase.as_view(), name='prodi-dosen-homebase'),
    path('prodi/dosen-penghitung-ratio/<str:id_prodi>/<str:id_thsmt>/', views.ProdiDosenPenghitungRatio.as_view(), name='prodi-dosen-penghitung-ratio'),
    
    # dosen
    path('dosen/profile/<str:id_dosen>/', views.DosenProfile.as_view(), name='dosen-profile'),
    path('dosen/study-history/<str:id_dosen>/', views.DosenRiwayatPendidikan.as_view(), name='dosen-riwayat-pendidikan'),
    path('dosen/dosen/teaching-history/<str:id_dosen>/', views.DosenRiwayatMengajar.as_view(), name='dosen-riwayat-mengajar'),
    path('dosen/portofolio/penelitian/<str:id_dosen>/', views.DosenPortofolioPenelitian.as_view(), name='dosen-portofolio-penelitian'),
    path('dosen/portofolio/pengabdian/<str:id_dosen>/', views.DosenPortofolioPengabdian.as_view(), name='dosen-portofolio-pengabdian'),
    path('dosen/portofolio/karya/<str:id_dosen>/', views.DosenPortofolioKarya.as_view(), name='dosen-portofolio-karya'),
    path('dosen/portofolio/paten/<str:id_dosen>/', views.DosenPortofolioPaten.as_view(), name='dosen-portofolio-paten'),
    
    # mahasiswa
    path('mhs/detail/<str:id_mhs>/', views.MhsDetail.as_view(), name='mhs-detail'),
    
    # statistics
    # mahaasiswa
    path('mhs/count/', views.MhsCount.as_view(), name='mhs-count'),
    path('mhs/count-active/', views.MhsCountActive.as_view(), name='mhs-count-active'),
    path('mhs/count-gender/', views.MhsCountGender.as_view(), name='mhs-count-gender'),
    path('mhs/count-bidang-ilmu/', views.MhsCountBidangIlmu.as_view(), name='mhs-count-bidang-ilmu'),
    path('mhs/count-status/', views.MhsCountStatus.as_view(), name='mhs-count-status'),
    path('mhs/count-jenjang/', views.MhsCountJenjang.as_view(), name='mhs-count-jenjang'),
    path('mhs/count-kelompok-lembaga/', views.MhsCountKelompokLembaga.as_view(), name='mhs-count-kelompok-lembaga'),
    
    # dosen
    path('dosen/count/', views.DosenCount.as_view(), name='dosen-count'),
    path('dosen/count-active/', views.DosenCountActive.as_view(), name='dosen-count-active'),
    path('dosen/count-gender/', views.DosenCountGender.as_view(), name='dosen-count-gender'),
    path('dosen/count-bidang/', views.DosenCountBidang.as_view(), name='dosen-count-bidang'),
    path('dosen/count-keaktifan/', views.DosenCountKeaktifan.as_view(), name='dosen-count-keaktifan'),
    path('dosen/count-jenjang/', views.DosenCountJenjang.as_view(), name='dosen-count-jenjang'),
    path('dosen/count-ikatan/', views.DosenCountIkatan.as_view(), name='dosen-count-ikatan'),
    
    # pt
    path('pt/count/', views.PTCount.as_view(), name='pt-count'),
    path('pt/count-province/', views.PTProvinceCount.as_view(), name='pt-count-province'),
    path('pt/count-kelompok-pembina/', views.PTKelompokPembinaCount.as_view(), name='pt-kelompok-pembina-count'),
    path('pt/count-akreditasi/', views.PTAkreditasiCount.as_view(), name='pt-akreditasi-count'),
    path('pt/count-bentuk-pt/', views.PTBentukPerguruanTinggiCount.as_view(), name='pt-bentuk-pt-count'),
]
