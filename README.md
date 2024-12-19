# PDDIKTI API

[![wakatime](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/e637f4e3-a75d-49c8-beb0-0f19f8eb52cd.svg)](https://wakatime.com/badge/user/018b799e-de53-4f7a-bb65-edc2df9f26d8/project/e637f4e3-a75d-49c8-beb0-0f19f8eb52cd)

## INFO

> **INFO:** The API has been updated based on new url <https://pddikti.kemdiktisaintek.go.id/>

## How to use?

read documentation at this [https://api-pddikti.vercel.app](https://api-pddikti.vercel.app)

## Overview

![API Overview](images/api-overview.png)

---

## API Documentation

## API Overview

- **Endpoint:** `/`
  - **Name:** `api-overview`
  - **Method:** `GET`
  - **Description:** Provides an overview of the available API endpoints.

## Search

### Search All

- **Endpoint:** `/search/all/{keyword}/`
  - **Name:** `search-all`
  - **Method:** `GET`
  - **Description:** Searches across all entities with the given keyword.
  - **Parameters:**
    - `keyword`: `string`

### Search Perguruan Tinggi (PT)

- **Endpoint:** `/search/pt/{keyword}/`
  - **Name:** `search-pt`
  - **Method:** `GET`
  - **Description:** Searches for Perguruan Tinggi with the given keyword.
  - **Parameters:**
    - `keyword`: `string`

### Search Program Studi (Prodi)

- **Endpoint:** `/search/prodi/{keyword}/`
  - **Name:** `search-prodi`
  - **Method:** `GET`
  - **Description:** Searches for Program Studi with the given keyword.
  - **Parameters:**
    - `keyword`: `string`

### Search Dosen

- **Endpoint:** `/search/dosen/{keyword}/`
  - **Name:** `search-dosen`
  - **Method:** `GET`
  - **Description:** Searches for Dosen with the given keyword.
  - **Parameters:**
    - `keyword`: `string`

### Search Mahasiswa

- **Endpoint:** `/search/mhs/{keyword}/`
  - **Name:** `search-mahasiswa`
  - **Method:** `GET`
  - **Description:** Searches for Mahasiswa with the given keyword.
  - **Parameters:**
    - `keyword`: `string`

## Perguruan Tinggi (PT)

### PT Detail

- **Endpoint:** `/pt/detail/{id_pt}/`
  - **Name:** `pt-detail`
  - **Method:** `GET`
  - **Description:** Retrieves detailed information about a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Prodi

- **Endpoint:** `/pt/prodi/{id_pt}/{id_thsmt}/`
  - **Name:** `pt-prodi`
  - **Method:** `GET`
  - **Description:** Retrieves the list of Program Studi within a Perguruan Tinggi for a specific semester.
  - **Parameters:**
    - `id_pt`: `string`
    - `id_thsmt`: `string`

### PT Rasio

- **Endpoint:** `/pt/rasio/{id_pt}/`
  - **Name:** `pt-rasio`
  - **Method:** `GET`
  - **Description:** Retrieves the student-to-lecturer ratio for a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Mahasiswa

- **Endpoint:** `/pt/mahasiswa/{id_pt}/`
  - **Name:** `pt-mahasiswa`
  - **Method:** `GET`
  - **Description:** Retrieves the average graduation rate of new students for a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Waktu Studi

- **Endpoint:** `/pt/waktu-studi/{id_pt}/`
  - **Name:** `pt-waktu-studi`
  - **Method:** `GET`
  - **Description:** Retrieves the average study duration of a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Riwayat

- **Endpoint:** `/pt/riwayat/{id_pt}/`
  - **Name:** `pt-riwayat`
  - **Method:** `GET`
  - **Description:** Retrieves the history of a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Biaya Kuliah

- **Endpoint:** `/pt/biaya-kuliah/{id_pt}/`
  - **Name:** `pt-biaya-kuliah`
  - **Method:** `GET`
  - **Description:** Retrieves the tuition fee information for a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Fasilitas

- **Endpoint:** `/pt/fasilitas/{id_pt}/`
  - **Name:** `pt-fasilitas`
  - **Method:** `GET`
  - **Description:** Retrieves the facilities information for a Perguruan Tinggi.
  - **Parameters:**
    - `id_pt`: `string`

### PT Logo

- **Endpoint:** `/pt/logo/{id_pt}/`
  - **Name:** `pt-logo`
  - **Method:** `GET`
  - **Description:** Retrieves the logo of a Perguruan Tinggi.
    -  **Parameters:**
    - `id_pt`: `string`

## Program Studi (Prodi)

### Prodi Detail

- **Endpoint:** `/prodi/detail/{id_prodi}/`
  - **Name:** `prodi-detail`
  - **Method:** `GET`
  - **Description:** Retrieves detailed information about a Program Studi.
  - **Parameters:**
    - `id_prodi`: `string`

### Prodi Description

- **Endpoint:** `/prodi/desc/{id_prodi}/`
  - **Name:** `prodi-desc`
  - **Method:** `GET`
  - **Description:** Retrieves description of a Program Studi.
    -  **Parameters:**
    - `id_prodi`: `string`
  
### Prodi Jumlah MHS Dosen
- **Endpoint:** `/prodi/num-students-lecturers/{id_prodi}/`
  - **Name:** `prodi-num-students-lecturers`
  - **Method:** `GET`
  - **Description:** Retrieves number of student and lecturer in a Program Studi.
  - **Parameters:**
    - `id_prodi`: `string`

### Prodi Riwayat

- **Endpoint:** `/prodi/riwayat/{id_prodi}/`
  - **Name:** `prodi-riwayat`
  - **Method:** `GET`
  - **Description:** Retrieves the history of a Program Studi.
  -  **Parameters:**
    - `id_prodi`: `string`

### Prodi Biaya Kuliah

- **Endpoint:** `/prodi/biaya-kuliah/{id_prodi}/`
  - **Name:** `prodi-biaya-kuliah`
  - **Method:** `GET`
  - **Description:** Retrieves the tuition fee information for a Program Studi.
    -  **Parameters:**
    - `id_prodi`: `string`

### Prodi Dosen Homebase

- **Endpoint:** `/prodi/dosen-homebase/{id_prodi}/{id_thsmt}/`
  - **Name:** `prodi-dosen-homebase`
  - **Method:** `GET`
  - **Description:** Retrieves the list of lecturers with homebase in Program Studi for a specific semester.
  - **Parameters:**
    - `id_prodi`: `string`
    - `id_thsmt`: `string`
    
### Prodi Dosen Penghitung Ratio
- **Endpoint:** `/prodi/dosen-penghitung-ratio/{id_prodi}/{id_thsmt}/`
  - **Name:** `prodi-dosen-penghitung-ratio`
  - **Method:** `GET`
  -  **Description:** Retrieves the list of lecturers that is counted for student lecturer ratio in Program Studi for a specific semester.
  - **Parameters:**
      - `id_prodi`: `string`
      - `id_thsmt`: `string`

## Dosen

### Dosen Profile

- **Endpoint:** `/dosen/profile/{id_dosen}/`
  - **Name:** `dosen-profile`
  - **Method:** `GET`
  - **Description:** Retrieves the profile information for a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

### Dosen Study History
- **Endpoint:** `/dosen/study-history/{id_dosen}/`
    - **Name:** `dosen-riwayat-pendidikan`
    - **Method:** `GET`
    - **Description:** Retrieves the education history of a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

### Dosen Teaching History
- **Endpoint:** `/dosen/dosen/teaching-history/{id_dosen}/`
  - **Name:** `dosen-riwayat-mengajar`
  - **Method:** `GET`
  - **Description:** Retrieves the teaching history of a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

### Dosen Portofolio Penelitian

- **Endpoint:** `/dosen/portofolio/penelitian/{id_dosen}/`
  - **Name:** `dosen-portofolio-penelitian`
  - **Method:** `GET`
  - **Description:** Retrieves the research portfolio of a Dosen.
   - **Parameters:**
    - `id_dosen`: `string`

### Dosen Portofolio Pengabdian

- **Endpoint:** `/dosen/portofolio/pengabdian/{id_dosen}/`
  - **Name:** `dosen-portofolio-pengabdian`
  - **Method:** `GET`
  - **Description:** Retrieves the community service portfolio of a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

### Dosen Portofolio Karya

- **Endpoint:** `/dosen/portofolio/karya/{id_dosen}/`
  - **Name:** `dosen-portofolio-karya`
  - **Method:** `GET`
  - **Description:** Retrieves the work portfolio of a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

### Dosen Portofolio Paten

- **Endpoint:** `/dosen/portofolio/paten/{id_dosen}/`
  - **Name:** `dosen-portofolio-paten`
  - **Method:** `GET`
  - **Description:** Retrieves the patent portfolio of a Dosen.
    -  **Parameters:**
    - `id_dosen`: `string`

## Mahasiswa

### Mahasiswa Detail

- **Endpoint:** `/mhs/detail/{id_mhs}/`
  - **Name:** `mhs-detail`
  - **Method:** `GET`
  - **Description:** Retrieves the detail of mahasiswa.
    -  **Parameters:**
    - `id_mhs`: `string`

## Statistics

### Mahasiswa Statistics

#### Total Mahasiswa Count

-   **Endpoint:** `/mhs/count/`
    -   **Name:** `mhs-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the total count of Mahasiswa.

#### Active Mahasiswa Count

-   **Endpoint:** `/mhs/count-active/`
    -   **Name:** `mhs-count-active`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of active Mahasiswa.

#### Mahasiswa Count by Gender

-   **Endpoint:** `/mhs/count-gender/`
    -   **Name:** `mhs-count-gender`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Mahasiswa based on gender.

#### Mahasiswa Count by Field of Study

-   **Endpoint:** `/mhs/count-bidang-ilmu/`
    -   **Name:** `mhs-count-bidang-ilmu`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Mahasiswa based on the field of study.
    
#### Mahasiswa Count by Status
-   **Endpoint:** `/mhs/count-status/`
    -   **Name:** `mhs-count-status`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Mahasiswa based on their status.

#### Mahasiswa Count by Jenjang
-   **Endpoint:** `/mhs/count-jenjang/`
    -   **Name:** `mhs-count-jenjang`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Mahasiswa based on their level of education.

#### Mahasiswa Count by Kelompok Lembaga
-   **Endpoint:** `/mhs/count-kelompok-lembaga/`
    -   **Name:** `mhs-count-kelompok-lembaga`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Mahasiswa based on their institutional group.

### Dosen Statistics

#### Total Dosen Count

-   **Endpoint:** `/dosen/count/`
    -   **Name:** `dosen-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the total count of Dosen.

#### Active Dosen Count
-    **Endpoint:** `/dosen/count-active/`
    -    **Name:** `dosen-count-active`
    -    **Method:** `GET`
    -    **Description:** Retrieves the count of active Dosen.

#### Dosen Count by Gender

-   **Endpoint:** `/dosen/count-gender/`
    -   **Name:** `dosen-count-gender`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Dosen based on gender.

#### Dosen Count by Field

-   **Endpoint:** `/dosen/count-bidang/`
    -   **Name:** `dosen-count-bidang`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Dosen based on their field.

#### Dosen Count by Keaktifan
-   **Endpoint:** `/dosen/count-keaktifan/`
    -   **Name:** `dosen-count-keaktifan`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Dosen based on their activeness status.

#### Dosen Count by Jenjang
-   **Endpoint:** `/dosen/count-jenjang/`
    -   **Name:** `dosen-count-jenjang`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Dosen based on their educational level.

#### Dosen Count by Ikatan
-   **Endpoint:** `/dosen/count-ikatan/`
    -   **Name:** `dosen-count-ikatan`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Dosen based on their employment status.

### PT Statistics

#### Total PT Count

-   **Endpoint:** `/pt/count/`
    -   **Name:** `pt-count`
    -   **Method:** `GET`
    -  **Description:** Retrieves the total count of Perguruan Tinggi.

#### PT Count by Province
-    **Endpoint:** `/pt/count-province/`
    -    **Name:** `pt-count-province`
    -    **Method:** `GET`
    -    **Description:** Retrieves the count of Perguruan Tinggi based on province.

#### PT Count by Kelompok Pembina

-   **Endpoint:** `/pt/count-kelompok-pembina/`
    -   **Name:** `pt-kelompok-pembina-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Perguruan Tinggi based on their supervisory group.

#### PT Count by Akreditasi

-   **Endpoint:** `/pt/count-akreditasi/`
    -   **Name:** `pt-akreditasi-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Perguruan Tinggi based on accreditation.

#### PT Count by Bentuk PT

-   **Endpoint:** `/pt/count-bentuk-pt/`
    -   **Name:** `pt-bentuk-pt-count`
    -   **Method:** `GET`
    -  **Description:** Retrieves the count of Perguruan Tinggi based on its type.

### Prodi Statistics

#### Total Prodi Count

-   **Endpoint:** `/prodi/count/`
    -   **Name:** `prodi-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the total count of Program Studi.

#### Prodi Bidang Ilmu Terbanyak Count
-  **Endpoint:** `/prodi/bidang-ilmu-terbanyak/`
   -   **Name:** `prodi-bidang-ilmu-terbanyak-count`
   -    **Method:** `GET`
   -    **Description:** Retrieves the count of Program Studi based on the most numerous field.

#### Prodi Count by Kelompok Pembina
-   **Endpoint:** `/prodi/kelompok-pembina/`
   -   **Name:** `prodi-kelompok-pembina-count`
    -   **Method:** `GET`
    -    **Description:** Retrieves the count of Program Studi based on the supervising group.
    
#### Prodi Count by Bidang Ilmu

-   **Endpoint:** `/prodi/bidang-ilmu/`
    -   **Name:** `prodi-bidang-ilmu-count`
    -   **Method:** `GET`
    -   **Description:** Retrieves the count of Program Studi based on their field.

#### Prodi Count by Akreditasi

-   **Endpoint:** `/prodi/akreditasi/`
    -   **Name:** `prodi-akreditasi-count`
    -   **Method:** `GET`
    -  **Description:** Retrieves the count of Program Studi based on their accreditation.
    
#### Prodi Count by Jenjang
-  **Endpoint:** `/prodi/jenjang/`
   -   **Name:** `prodi-jenjang-count`
   -   **Method:** `GET`
   -  **Description:** Retrieves the count of Program Studi based on their educational level.

## Prodi by Bidang Ilmu

### Prodi Agama
-  **Endpoint:** `/prodi/bidang-ilmu/agama/`
    -   **Name:** `prodi-bidang-ilmu-agama`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Agama.
    
### Prodi Ekonomi
-  **Endpoint:** `/prodi/bidang-ilmu/ekonomi/`
    -   **Name:** `prodi-bidang-ilmu-ekonomi`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Ekonomi.

### Prodi Humaniora
-  **Endpoint:** `/prodi/bidang-ilmu/humaniora/`
    -   **Name:** `prodi-bidang-ilmu-humaniora`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Humaniora.

### Prodi Kesehatan
-  **Endpoint:** `/prodi/bidang-ilmu/kesehatan/`
    -   **Name:** `prodi-bidang-ilmu-kesehatan`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Kesehatan.
    
### Prodi MIPA
-  **Endpoint:** `/prodi/bidang-ilmu/mipa/`
    -   **Name:** `prodi-bidang-ilmu-mipa`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as MIPA.
    
### Prodi Pendidikan
-  **Endpoint:** `/prodi/bidang-ilmu/pendidikan/`
    -   **Name:** `prodi-bidang-ilmu-pendidikan`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Pendidikan.

### Prodi Pertanian
-  **Endpoint:** `/prodi/bidang-ilmu/pertanian/`
    -   **Name:** `prodi-bidang-ilmu-pertanian`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Pertanian.

### Prodi Seni
-  **Endpoint:** `/prodi/bidang-ilmu/seni/`
    -   **Name:** `prodi-bidang-ilmu-seni`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Seni.
    
### Prodi Sosial
-  **Endpoint:** `/prodi/bidang-ilmu/sosial/`
    -   **Name:** `prodi-bidang-ilmu-sosial`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Sosial.

### Prodi Teknik
-  **Endpoint:** `/prodi/bidang-ilmu/teknik/`
    -   **Name:** `prodi-bidang-ilmu-teknik`
    -   **Method:** `GET`
    -   **Description:** Retrieves the list of Program Studi that categorized as Teknik.