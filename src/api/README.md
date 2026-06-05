# HRSS Recommendation API

Direktori `src/api/` berisi implementasi backend web service menggunakan **FastAPI**. Layanan ini dirancang menggunakan pola *Offline Baking*, di mana server membaca file model statis (`.pkl`) dari disk lokal, menjadikannya sangat cepat, mandiri, dan andal di lingkungan jaringan operasional pabrik.

## 🚀 Menjalankan Server Lokal (Development)

Pastikan Anda berada di root direktori proyek, lalu jalankan Uvicorn:

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

> **Catatan MLOps**: Jika saat server dijalankan muncul *error* gagal *startup* karena model `.pkl` tidak ditemukan, pastikan Anda telah menjalankan skrip `python -m src.scripts.export_champion` terlebih dahulu untuk mengunduh versi terbaik model dari MLflow ke sistem lokal.

---

## 🌐 Endpoints Utama

API ini dirancang untuk menerima data telemetri HRSS dan mengembalikan hasil klasifikasi (Machine Learning) beserta rekomendasi perbaikan tindakan. Dokumentasi interaktif Swagger otomatis tersedia di `http://localhost:8000/docs`.

### 1. `GET /health`
Mengecek apakah API server menyala dan model lokal berhasil dimuat. Digunakan oleh probe Kubernetes atau Docker *healthcheck*.

### 2. `POST /predict`
Mengirim data telemetri satu baris dan mengembalikan *raw prediction* (0: Standard, 1: Optimized) beserta skor probabilitas.

### 3. `POST /recommend`
Endpoint tercanggih yang menggabungkan hasil Machine Learning dan *Rule Engine* bisnis.
* **Input Payload**: Data JSON yang setara dengan satu baris fitur HRSS.
* **Output Response**: Menyediakan probabilitas model, sinyal deteksi anomali rule-based (misal: "Voltage Sag" atau "Rail Inefficiency"), tingkat risiko, dan **Actionable Recommendation** (saran perbaikan operasional kepada operator di pabrik).

## 🧩 Arsitektur Folder `api/`
* **`main.py`**: Entrypoint FastAPI, mengatur inisialisasi lifecycle dan memuat model ke memory.
* **`routes/`**: Kumpulan definisi HTTP Endpoint yang dibagi berdasarkan fungsinya (Prediction, Recommendation, Health).
* **`schemas/`**: Menggunakan Pydantic Models untuk memvalidasi secara ketat skema input dari user dan menyusun format output respons API.
