"""
Feature Engineering — Membuat fitur turunan dari data telemetry HRSS.

Semua kalkulasi fitur didefinisikan di sini sebagai satu-satunya
sumber kebenaran, digunakan baik saat training maupun inference.

PENTING: Kolom `I_w_*_Weg` berisi koordinat posisi absolut (bukan
jarak tempuh/kecepatan). Dalam arsitektur stateless (row-by-row),
kita tidak bisa menghitung delta posisi antar-timestep. Oleh karena
itu, fitur turunan yang valid hanya berasal dari Power dan Voltage.
"""
import pandas as pd
import logging

from src.core.problem_definition import (
    POWER_COLUMNS, VOLTAGE_COLUMNS,
)

logger = logging.getLogger(__name__)

EPSILON = 1e-9  # Pencegah division by zero
MOTOR_ACTIVE_THRESHOLD = 100  # Watt — motor dianggap aktif jika daya > 100W


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membuat fitur-fitur turunan dari kolom sensor mentah:
    - total_power:         Jumlah konsumsi daya seluruh sumbu (Watt)
    - avg_voltage:         Rata-rata tegangan seluruh sumbu (Volt)
    - active_motor_count:  Jumlah motor yang aktif (power > threshold)
    """
    df = df.copy()

    df["total_power"] = df[POWER_COLUMNS].sum(axis=1)
    df["avg_voltage"] = df[VOLTAGE_COLUMNS].mean(axis=1)
    df["active_motor_count"] = (df[POWER_COLUMNS] > MOTOR_ACTIVE_THRESHOLD).sum(axis=1)

    logger.info("Feature engineering complete. New columns added. Shape: %s", df.shape)
    return df

