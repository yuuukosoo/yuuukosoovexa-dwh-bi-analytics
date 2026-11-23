# PT YuuukosooVexa — Data Warehouse & Business Intelligence Analytics

Proyek Data Warehouse dan Business Intelligence *end-to-end* untuk studi kasus **PT YuuukosooVexa** (ritel *e-commerce* suplemen kesehatan dan kebugaran multi-kanal) pada Mata Kuliah Kecerdasan Bisnis, Peminatan Manajemen Teknologi Informasi (MTI), Program Studi Teknologi Informasi, Fakultas Teknik, Universitas Lambung Mangkurat (ULM).

## Identitas Mahasiswa

- **Nama:** Muhammad Naufal Khalish
- **NIM:** 2410817110004
- **Peminatan:** Manajemen Teknologi Informasi (MTI)

## Arsitektur Sistem

```
Multi-Source Raw CSV (942,554 baris)
        │
        ▼  etl/01_preprocess_raw.py
Processed Clean CSV (10 file, 9.37 MB)
        │
        ▼  etl/02_load_staging.py → etl/03_transform_dwh.py
PostgreSQL 16.16 Data Warehouse (105,811 baris: 6 Dimensi + 4 Fakta)
        │
        ▼  sql/04_create_datamarts.sql (5 Views + 6 RBAC Roles)
Data Marts (datamart.vw_*)  ──►  Apache Airflow 2.10.4 Orchestration
        │
        ▼  dashboard/Streamlit/app.py (Live DWH + Cloud Snapshot Fallback)
Interactive BI Dashboard (Streamlit + Plotly, Light/Dark, Bilingual ID/EN)
```

## Fitur Utama Dashboard BI

1. **Executive Summary** — KPI eksekutif (`INR 53.68M` Net Revenue, `50,000` transaksi, `82,123` unit, rata-rata diskon `22.06%`), tren pendapatan *Net vs Gross*, distribusi kategori, dan *donut chart* pangsa kanal (`Flipkart Health` 56.0% vs `Tata 1mg` 44.0%).
2. **Sales & Pricing** — *Heatmap* elastisitas diskon per kategori, pendapatan per pita diskon, tabel *Top 50 Product SKUs* dengan *live search*, serta *drill-through* **Product SKU Deep-Dive**.
3. **Environmental AQI** — Peta interaktif 29 kota India (*Esri Gray Canvas*), korelasi *AQI vs Vitamin Revenue*, peringkat 8 kota berpolusi tertinggi, serta *drill-through* **City AQI Diagnostic**.
4. **Lifestyle & Fitness** — Segmentasi 80.000 profil *gym* berdasarkan *BMI* (*stacked card deck*), *Wellness Profile Radar* 6 dimensi, dan sebaran gangguan tidur menurut profesi.

## Menjalankan Secara Lokal

### 1. Mode Cloud / Tanpa Docker (Langsung Jalankan Dashboard)

```bash
pip install -r requirements.txt
streamlit run dashboard/Streamlit/app.py
```

*Dashboard* otomatis membaca *snapshot* `data/processed/` jika PostgreSQL lokal tidak aktif.

### 2. Mode Penuh dengan Docker (PostgreSQL 16 + pgAdmin + Apache Airflow)

```bash
cp .env.example .env
docker compose up -d
python etl/01_preprocess_raw.py
python etl/02_load_staging.py
python etl/03_transform_dwh.py
python etl/05_validate_dwh.py
streamlit run dashboard/Streamlit/app.py
```

> Catatan: File mentah `INDIA_AQI_COMPLETE_20251126.csv` (269.53 MB) dikecualikan dari *repository* karena melebihi batas 100 MB GitHub. Hasil pra-pemrosesan lengkap tersedia pada `data/processed/`.
