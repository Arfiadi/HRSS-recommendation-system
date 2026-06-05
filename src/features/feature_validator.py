"""
Feature Validator — Memvalidasi kualitas fitur sebelum masuk ke model.

Memastikan bahwa DataFrame yang akan di-inferensikan memiliki
semua kolom yang dibutuhkan model dan tidak ada nilai null.
"""
import pandas as pd
import logging

from src.core.problem_definition import MODEL_FEATURE_COLUMNS

logger = logging.getLogger(__name__)


def validate_features(df: pd.DataFrame, expected_columns: list = None) -> bool:
    """
    Mengecek apakah DataFrame berisi semua kolom fitur yang dibutuhkan
    dan tidak memiliki nilai null.

    Args:
        df: DataFrame yang akan divalidasi.
        expected_columns: Daftar kolom yang diharapkan ada.
                          Default menggunakan MODEL_FEATURE_COLUMNS.

    Returns:
        True jika valid, False jika tidak.
    """
    if expected_columns is None:
        expected_columns = MODEL_FEATURE_COLUMNS

    missing = [c for c in expected_columns if c not in df.columns]
    if missing:
        logger.error("Feature validation FAILED — missing columns: %s", missing)
        return False

    null_count = df[expected_columns].isnull().sum().sum()
    if null_count > 0:
        logger.warning(
            "Feature validation WARNING — %d null values found in feature columns",
            null_count,
        )
        return False

    logger.info("Feature validation PASSED. All %d columns present, 0 nulls.", len(expected_columns))
    return True
