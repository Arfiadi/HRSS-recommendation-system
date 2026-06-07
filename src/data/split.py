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

    # Chronological Split per class to prevent Time-Series Leakage
    train_dfs = []
    test_dfs = []
    
    for op_type in df[TARGET_COLUMN].unique():
        class_df = df[df[TARGET_COLUMN] == op_type].copy()
        split_idx = int(len(class_df) * (1 - test_size))
        
        train_dfs.append(class_df.iloc[:split_idx])
        test_dfs.append(class_df.iloc[split_idx:])
        
    train_df = pd.concat(train_dfs, ignore_index=True)
    test_df = pd.concat(test_dfs, ignore_index=True)
    
    X_train = train_df[MODEL_FEATURE_COLUMNS]
    y_train = train_df[[TARGET_COLUMN]]
    X_test = test_df[MODEL_FEATURE_COLUMNS]
    y_test = test_df[[TARGET_COLUMN]]

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
