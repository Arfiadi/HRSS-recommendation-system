"""
Data Ingestion — Memuat data mentah HRSS dari sumber.

File ini akan berisi:
- Fungsi untuk membaca CSV raw dari folder data/raw/
- Penggabungan dataset standard dan optimized dengan label operation_type
- Validasi dasar (cek kolom, cek tipe data, cek missing values)

Contoh fungsi:
    def load_raw_datasets(raw_dir: str) -> pd.DataFrame:
        \'\'\'
        Membaca HRSS_normal_standard.csv dan HRSS_normal_optimized.csv,
        menambahkan kolom operation_type (0=standard, 1=optimized),
        lalu menggabungkannya menjadi satu DataFrame.
        \'\'\'
        pass

    def validate_raw_data(df: pd.DataFrame) -> bool:
        \'\'\'Validasi bahwa kolom-kolom yang diharapkan ada di dataset.\'\'\'
        pass

TODO: Implement data ingestion functions.
"""
