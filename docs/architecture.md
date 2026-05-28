# Arsitektur Sistem

## Industrial Operational Recommendation System (HRSS)

---

# 1. Gambaran Umum Sistem

Proyek ini merupakan **Sistem Rekomendasi Keputusan Operasional Industri berbasis data telemetry** dari High Rack Storage System (HRSS).

Tujuan utama sistem ini adalah:

* Mengklasifikasikan jenis operasi (standard vs optimized)
* Menganalisis pola konsumsi energi dan aktivitas movement
* Mengidentifikasi perilaku operasional yang efisien
* Menghasilkan rekomendasi peningkatan efisiensi operasional

Sistem ini tidak hanya berfokus pada machine learning model, tetapi pada **sistem pengambilan keputusan berbasis data industri**.

---

# 2. Arsitektur Tingkat Tinggi

Sistem dibangun dengan pendekatan berlapis (layered architecture):

```
Data Layer → Feature Layer → Model Layer → Service Layer → Interface Layer
```

---

## 2.1 Alur Sistem End-to-End

```
Data Telemetry HRSS
        ↓
Data Cleaning & Preprocessing
        ↓
Feature Engineering
        ↓
Train-Test Split (Controlled)
        ↓
Eksperimen Model (PyCaret + MLflow)
        ↓
Pemilihan Model Terbaik
        ↓
Inference Service
        ↓
Recommendation Engine
        ↓
Streamlit Dashboard
```

---

# 3. Komponen Sistem

## 3.1 Data Layer

Layer ini bertanggung jawab untuk pengelolaan data mentah dan data hasil transformasi.

Komponen:

* Dataset raw HRSS (normal & anomalous)
* Dataset processed (cleaned & engineered)
* Dataset splits (train/test)

Prinsip utama:

* Tidak boleh ada data leakage
* Reproducibility harus terjaga
* Pemisahan jelas antara raw dan processed data

---

## 3.2 Feature Layer

Layer ini bertugas membentuk representasi data yang lebih informatif.

Contoh fitur:

* total_power
* avg_voltage
* total_movement
* rail_activity
* conveyor_activity
* energy efficiency ratio

Tujuan:
Mengubah data telemetry menjadi representasi perilaku operasional.

---

## 3.3 Model Layer

Layer ini menangani proses machine learning untuk klasifikasi biner.

Target:

* operation_type

  * 0 = standard operation
  * 1 = optimized operation

Model yang digunakan:

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost

Pendekatan eksperimen:

* PyCaret untuk perbandingan model cepat
* MLflow untuk tracking eksperimen

---

## 3.4 Service Layer (Inti Sistem)

Ini adalah lapisan paling penting dalam sistem.

Komponen:

* inference_service
* prediction_pipeline
* recommendation_service

Fungsi utama:

* Menggabungkan preprocessing + model inference
* Menyediakan output terstruktur
* Menjalankan logika rekomendasi

Lapisan ini memastikan bahwa:

> Model dapat diganti tanpa merusak sistem secara keseluruhan

---

## 3.5 Recommendation Layer

Layer ini mengubah hasil prediksi menjadi insight yang dapat ditindaklanjuti.

Pendekatan:

* Rule-based logic
* Decision policy berbasis risiko

Output:

* Deteksi ketidakefisienan operasi
* Indikasi pemborosan energi
* Saran optimasi operasional

---

## 3.6 Interface Layer

Layer ini merupakan antarmuka pengguna berbasis Streamlit.

Halaman utama:

* Overview sistem
* Prediction (simulasi inference)
* Recommendation
* Perbandingan model (RAW vs ENGINEERED)
* Explainability

Tujuan:
Menyajikan sistem dalam bentuk yang mudah dipahami dan digunakan.

---

# 4. Desain Eksperimen

Terdapat dua pipeline utama:

## 4.1 Pipeline Raw Feature

* Menggunakan fitur asli dari dataset
* Menjadi baseline performa model

## 4.2 Pipeline Engineered Feature

* Menggunakan fitur hasil feature engineering
* Meningkatkan representasi perilaku operasional

Tujuan perbandingan:

> Mengukur dampak feature engineering terhadap performa model

---

# 5. Strategi Evaluasi

## Metrik Utama:

* F1-score (macro)
* ROC-AUC

## Metrik Sekunder:

* Precision (kelas optimized)
* Recall (kelas optimized)

## Metrik Risiko:

* False Negative Rate (FNR)
* False Positive Rate (FPR)

Interpretasi:

* Fokus tidak hanya pada akurasi, tetapi pada kualitas keputusan operasional

---

# 6. Prinsip Desain Sistem

* Separation of concerns (data, model, service, UI)
* Reproducibility melalui fixed data splits
* Model-agnostic inference layer
* Experiment-driven development
* Interpretabilitas dalam konteks industri

---

# 7. Arah Pengembangan ke Depan

## Tahap 1 (Saat Ini)

* Sistem analisis offline berbasis notebook
* Model klasifikasi + rekomendasi dasar

## Tahap 2 (Pengembangan Lanjut)

* API inference (FastAPI)
* Model registry (versioning)
* Inference real-time

## Tahap 3 (Skala Industri)

* Streaming telemetry data
* Feature store
* Monitoring model drift
* Sistem optimasi operasional real-time

---

# 8. Kesimpulan

Sistem ini bukan hanya proyek machine learning, tetapi:

> Sistem pengambilan keputusan operasional industri berbasis data telemetry dan machine learning

Fokus utama bukan hanya prediksi, tetapi **pengambilan keputusan berbasis efisiensi operasional**.
