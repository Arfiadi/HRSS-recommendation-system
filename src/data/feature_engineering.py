"""
Feature Engineering — Membuat fitur turunan dari data telemetry HRSS.

Semua kalkulasi fitur didefinisikan di sini sebagai satu-satunya
sumber kebenaran, digunakan baik saat training maupun inference.
"""
import pandas as pd
import logging

from src.core.problem_definition import (
    POWER_COLUMNS, VOLTAGE_COLUMNS, MOVEMENT_COLUMNS,
    RAIL_COLUMNS, CONVEYOR_COLUMNS,
)

logger = logging.getLogger(__name__)

EPSILON = 1e-9  # Pencegah division by zero


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membuat fitur-fitur turunan dari kolom sensor mentah:
    - total_power:              Jumlah konsumsi daya seluruh sumbu
    - avg_voltage:              Rata-rata tegangan seluruh sumbu
    - total_movement:           Jumlah pergerakan seluruh sumbu
    - power_efficiency_ratio:   Rasio pergerakan terhadap daya (efisiensi)
    - rail_activity:            Aktivitas pergerakan rel (sumbu HL dan HR)
    - conveyor_activity:        Aktivitas pergerakan konveyor (sumbu BLO, BHL, BHR, BRU)
    """
    df = df.copy()

    df["total_power"] = df[POWER_COLUMNS].sum(axis=1)
    df["avg_voltage"] = df[VOLTAGE_COLUMNS].mean(axis=1)
    df["total_movement"] = df[MOVEMENT_COLUMNS].sum(axis=1)
    df["power_efficiency_ratio"] = df["total_movement"] / (df["total_power"] + EPSILON)
    df["rail_activity"] = df[RAIL_COLUMNS].sum(axis=1)
    df["conveyor_activity"] = df[CONVEYOR_COLUMNS].sum(axis=1)

    logger.info("Feature engineering complete. New columns added. Shape: %s", df.shape)
    return df
