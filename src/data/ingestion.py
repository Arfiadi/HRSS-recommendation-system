"""
Data Ingestion — Memuat data mentah HRSS dari sumber.

Membaca CSV raw, menggabungkan dataset standard dan optimized
dengan label operation_type, dan melakukan validasi dasar.
"""
import os
import pandas as pd
import logging

from src.core.problem_definition import (
    RAW_FILES, TARGET_COLUMN, ALL_SENSOR_COLUMNS,
)

logger = logging.getLogger(__name__)


def load_raw_datasets(raw_dir: str) -> pd.DataFrame:
    """
    Membaca HRSS_normal_standard.csv dan HRSS_normal_optimized.csv,
    menambahkan kolom operation_type (0=standard, 1=optimized),
    lalu menggabungkannya menjadi satu DataFrame.
    """
    std_path = os.path.join(raw_dir, RAW_FILES["normal_standard"])
    opt_path = os.path.join(raw_dir, RAW_FILES["normal_optimized"])

    logger.info("Loading standard data from %s", std_path)
    df_std = pd.read_csv(std_path)
    df_std[TARGET_COLUMN] = 0

    logger.info("Loading optimized data from %s", opt_path)
    df_opt = pd.read_csv(opt_path)
    df_opt[TARGET_COLUMN] = 1

    df = pd.concat([df_std, df_opt], ignore_index=True)
    logger.info("Combined dataset shape: %s", df.shape)

    return df


def validate_raw_data(df: pd.DataFrame) -> bool:
    """Validasi bahwa kolom-kolom yang diharapkan ada di dataset."""
    missing = [c for c in ALL_SENSOR_COLUMNS if c not in df.columns]
    if missing:
        logger.error("Missing columns in raw data: %s", missing)
        return False

    null_counts = df[ALL_SENSOR_COLUMNS].isnull().sum().sum()
    if null_counts > 0:
        logger.warning("Found %d null values in sensor columns", null_counts)

    logger.info("Raw data validation passed. Shape: %s", df.shape)
    return True
