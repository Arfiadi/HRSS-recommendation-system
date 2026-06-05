# HRSS Recommendation System: Production System Design

Dokumen ini mendeskripsikan arsitektur sistem perangkat lunak (*software architecture*) dan desain sistem rekomendasi untuk fase *production* dari proyek HRSS. Desain ini dirancang untuk memastikan keandalan, skalabilitas, dan kemudahan pemeliharaan (*maintainability*) menggunakan standar praktik MLOps.

## 1. Arsitektur Sistem Global (High-Level Architecture)

Sistem *production* akan dibagi menjadi dua *pipeline* utama yang terpisah secara fisik maupun logis:

1. **Training Pipeline (Offline):** Berfungsi untuk melatih ulang model menggunakan data historis terbaru, membungkus proses *feature engineering* ke dalam satu objek utuh, dan menyimpannya ke Model Registry.
2. **Inference Pipeline & API (Online):** Berfungsi sebagai *Backend Server* yang siaga menerima data *streaming* dari sensor (IoT), memprosesnya secara instan, dan mengembalikan rekomendasi preskriptif ke *dashboard* operator.

---

## 2. Pemetaan Direktori & Komponen Utama (`src/`)

Seluruh kode *production* akan hidup di dalam direktori `src/`, dengan pembagian modul sebagai berikut:

### `src/features/`
- **Tujuan:** Menggantikan sel *Feature Engineering* di Notebook 02 menjadi *Class* Python murni.
- **Implementasi:** Kita akan membuat *Custom Scikit-Learn Transformers* (turunan dari `BaseEstimator, TransformerMixin`).
- **Keuntungan:** Semua transformasi (kalkulasi `total_power`, *handling missing values*) akan terbungkus rapi dan dapat digabungkan ke dalam `sklearn.pipeline.Pipeline`. Saat *inference*, kita tidak perlu memanggil fungsi *preprocessing* secara terpisah.

### `src/models/`
- **`train_model.py`:** Skrip untuk melatih model (*training loop*). Skrip ini akan secara otomatis menarik konfigurasi dari `configs/model_config.yaml`, melatih `Pipeline` (Preprocessing + Random Forest), dan **mengirimkan (log) model, metrik, dan parameter ke MLflow**.
- **`predict_model.py`:** Fungsi atau kelas *wrapper* yang memuat versi model terbaik dari *MLflow Registry* ke dalam memori untuk melakukan inferensi.

### `src/api/`
- **Tujuan:** Antarmuka komunikasi sistem (Web API).
- **Implementasi:** Menggunakan **FastAPI**.
- **`schemas.py`:** Mendefinisikan struktur *payload request* (menggunakan Pydantic) dari sensor IoT dan struktur *response* rekomendasi.
- **`main.py` / `routes.py`:** Mendefinisikan *endpoint* (misal: `POST /api/v1/recommend`) yang akan memanggil fungsi di `predict_model.py` dan `Recommendation Engine`.

---

## 3. Desain Recommendation Engine (Hybrid Architecture)

Sistem rekomendasi di tahap *production* tidak lagi mengandalkan probabilitas ML murni. Modul `Engine` ini adalah sebuah **Decision Support System (DSS)** kelas industri yang memadukan *Machine Learning* dan *Rule-Based Domain Knowledge*.

### 3.1. Komponen Evaluasi
1. **ML Model Branch (Probabilistik):** Menerima data sensor yang telah di-*preprocess* dan menebak profil operasional secara umum (probabilitas *Optimized* vs *Standard*).
2. **Rule Engine Branch (Deterministik):** Menganalisis parameter mekanis dan kelistrikan HRSS spesifik untuk mencari anomali:
   - **Rule Rail Inefficiency:** Aktivitas rel tinggi tetapi rasio efisiensi daya sangat rendah $\rightarrow$ *Indikasi masalah routing WMS*.
   - **Rule Mechanical Friction:** Tarikan daya/arus ekstrem dengan pergerakan statis/lambat $\rightarrow$ *Indikasi beban berlebih (overload) atau butuh pelumasan*.
   - **Rule Electrical Voltage Drop:** Anjloknya tegangan Bus DC $\rightarrow$ *Peringatan untuk menghindari akselerasi multi-sumbu serentak*.

### 3.2. Decision Policy Layer (The Combiner)
Alur logika pada API (seperti di fungsi `.recommend()`) akan menyatukan `Current Mode`, `ML Prediction`, dan `Rule Alerts` untuk menetapkan **Tingkat Risiko** dan tindakan preskriptif:

| Current Mode vs ML Prediction | Status Rule Alerts | Tingkat Risiko Operasional | Output Rekomendasi API (Final Action) |
| :--- | :--- | :--- | :--- |
| **Sesuai** (Tidak ada gap) | **Kosong** (Aman) | **Low Risk (Normal Operation)** | ✅ **Status Normal:** Beban ideal. Pertahankan pengaturan mode saat ini. |
| **Berbeda** (Ada gap prediksi) | **Kosong** (Aman) | **Medium Inefficiency** | 💡 **Rekomendasi Efisiensi:** Pola kelistrikan cocok untuk mode baru. Disarankan transisi mode. |
| (Tidak relevan) | **Terpicu** (Ada Anomali) | **High Inefficiency / Anomaly** | ⚠️ **Peringatan Darurat:** Beralih ke mode aman (Standard) & lakukan tindakan teknis spesifik (misal: "Inspeksi keausan rel"). |

---

## 4. Technology Stack (Production)
- **Machine Learning Core:** `scikit-learn` (Pipelines, RandomForest)
- **MLOps & Tracking:** `MLflow` (Tracking server & Model Registry)
- **API Framework:** `FastAPI` (High-performance web framework)
- **Data Validation:** `Pydantic` (Struktur input/output yang ketat)
- **Configuration Management:** `YAML` / `OmegaConf` / `Hydra` (Memisahkan *hardcoded variables* dari kode)

## 5. Rencana Eksekusi Selanjutnya
Setelah desain ini disetujui, kita akan mengeksekusi pembangunan kodenya secara bertahap:
1. Menulis *Custom Transformer* di `src/features/`.
2. Menulis skrip `train_model.py` dan mengintegrasikannya dengan MLflow.
3. Merakit *Recommendation Engine* dan *FastAPI Endpoint* di `src/api/`.
