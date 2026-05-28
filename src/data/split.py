"""
Data Split — Membagi dataset menjadi train/test dengan kontrol reprodusibilitas.

File ini akan berisi:
- Fungsi split dataset dengan fixed random seed
- Menyimpan hasil split ke folder data/splits/ sebagai single source of truth
- Fungsi load splits yang sudah tersimpan
- Memastikan tidak ada data leakage antara train dan test

Contoh fungsi:
    def create_and_save_splits(df, target_col, test_size=0.2, seed=42):
        \'\'\'
        Membagi dataset menjadi X_train, X_test, y_train, y_test
        dan menyimpannya ke data/splits/.
        \'\'\'
        pass

    def load_saved_splits(splits_dir: str):
        \'\'\'Memuat splits yang sudah tersimpan untuk reprodusibilitas.\'\'\'
        pass

TODO: Implement data splitting functions.
"""
