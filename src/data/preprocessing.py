"""
Data Preprocessing — Membersihkan dan mempersiapkan data HRSS.

Menangani missing values, duplikat, type casting,
dan drop kolom yang tidak diperlukan untuk modeling.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan data: handle missing values, duplicates,
    drop kolom 'Labels' (redundan dengan operation_type),
    dan memastikan tipe data kolom sudah benar.
    """
    initial_shape = df.shape
    logger.info("Starting data cleaning. Initial shape: %s", initial_shape)

    # Drop kolom 'Labels' jika ada (sudah diganti operation_type)
    if "Labels" in df.columns:
        df = df.drop(columns=["Labels"])
        logger.info("Dropped 'Labels' column (redundant with operation_type)")

    # Drop duplikat
    n_dup = df.duplicated().sum()
    if n_dup > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        logger.info("Dropped %d duplicate rows", n_dup)

    # Handle missing values — drop rows with any null in sensor columns
    n_null = df.isnull().sum().sum()
    if n_null > 0:
        df = df.dropna().reset_index(drop=True)
        logger.info("Dropped rows with null values (%d total nulls)", n_null)

    # Pastikan semua kolom numerik (kecuali Timestamp) bertipe float
    numeric_cols = [c for c in df.columns if c not in ["Timestamp", "operation_type"]]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info("Data cleaning complete. Final shape: %s", df.shape)
    return df
