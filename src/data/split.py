"""
Data Split — Membagi dataset menjadi train/test dengan kontrol reprodusibilitas.

Menyimpan hasil split ke folder data/splits/ sebagai single source of truth
dan menyediakan fungsi load untuk reprodusibilitas.
"""
import os
import pandas as pd
import logging
from sklearn.model_selection import train_test_split

from src.core.problem_definition import TARGET_COLUMN, MODEL_FEATURE_COLUMNS

logger = logging.getLogger(__name__)


def create_and_save_splits(
    df: pd.DataFrame,
    splits_dir: str,
    test_size: float = 0.2,
    seed: int = 42,
) -> tuple:
    """
    Membagi dataset menjadi X_train, X_test, y_train, y_test
    dan menyimpannya ke data/splits/.
    """
    os.makedirs(splits_dir, exist_ok=True)

    X = df[MODEL_FEATURE_COLUMNS]
    y = df[[TARGET_COLUMN]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y,
    )

    X_train.to_csv(os.path.join(splits_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(splits_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(splits_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(splits_dir, "y_test.csv"), index=False)

    logger.info(
        "Splits saved to %s — train: %d, test: %d",
        splits_dir, len(X_train), len(X_test),
    )
    return X_train, X_test, y_train.values.ravel(), y_test.values.ravel()


def load_saved_splits(splits_dir: str) -> tuple:
    """Memuat splits yang sudah tersimpan untuk reprodusibilitas."""
    X_train = pd.read_csv(os.path.join(splits_dir, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(splits_dir, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(splits_dir, "y_train.csv")).values.ravel()
    y_test = pd.read_csv(os.path.join(splits_dir, "y_test.csv")).values.ravel()

    logger.info(
        "Splits loaded from %s — train: %d, test: %d",
        splits_dir, len(X_train), len(X_test),
    )
    return X_train, X_test, y_train, y_test
