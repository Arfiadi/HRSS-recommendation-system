# Data Layer & Telemetry Schemas

Folder `data/` ini bertanggung jawab untuk menyimpan seluruh lifecycle dataset pada HRSS Recommendation System. 

> [!WARNING]
> Seluruh file data (terutama `.csv`) di dalam folder ini **diabaikan (ignored) oleh Git** melalui `.gitignore` untuk mencegah kebocoran data (data leakage) dan pembengkakan repositori. Pastikan Anda mengunduh dan menaruh raw data secara manual sebelum menjalankan training pipeline.

## 📂 Struktur Direktori

* **`raw/`**: Tempat meletakkan data mentah asli yang belum dimodifikasi dari sensor. File yang dibutuhkan:
  * `HRSS_normal_standard.csv` (Telemetri dengan pergerakan standar)
  * `HRSS_normal_optimized.csv` (Telemetri dengan pergerakan simultan yang dioptimasi)
* **`processed/`**: Menyimpan dataset hasil proses (telah dibersihkan dan dilakukan Feature Engineering).
* **`splits/`**: Menyimpan data yang telah dibagi untuk training dan testing (`X_train.csv`, `X_test.csv`, dll) secara deterministik untuk menjaga reproduktibilitas eksperimen.

## 📊 Skema Data Telemetri (Raw)

Dataset merepresentasikan output rekaman sensor sistem High Rack Storage secara time-series. Fitur-fitur utamanya meliputi:

* `operation_type`: Target utama / Label (0 = Standard, 1 = Optimized).
* **Power Columns**: Pengukuran konsumsi daya listrik dari berbagai komponen (misal: `O_w_BLO_power`, `O_w_BHL_power`, `O_w_HR_power`).
* **Voltage Columns**: Pengukuran voltase mesin.
* **Movement/Position Columns**: Menunjukkan metrik pergerakan di konveyor maupun rel (`I_w_BLO_Weg`, `I_w_HR_Weg`, dll).

Untuk penjelasan spesifik mengenai feature engineering, silakan merujuk pada `src/data/feature_engineering.py`.
