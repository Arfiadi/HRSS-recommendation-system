"""
Scoring — Sistem penilaian efisiensi operasional.

Menghitung skor efisiensi operasional dari rentang 0-100.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def calculate_efficiency_score(
    df: pd.DataFrame, probability_optimized: float, rule_alerts: list
) -> float:
    """
    Menghitung skor efisiensi 0-100 berdasarkan probabilitas optimasi ML
    dan penalti dari warning/alert yang terpicu.

    Args:
        df: DataFrame telemetry yang di-preprocess.
        probability_optimized: Probabilitas profil operasi Optimized (0.0 - 1.0).
        rule_alerts: List alert string dari Rule Engine.

    Returns:
        Skor efisiensi operasional (float 0.0 - 100.0).
    """
    # Base score adalah persentase probabilitas optimized (profil hemat energi)
    base_score = probability_optimized * 100.0

    # Pengurangan skor (penalti) jika ada rules yang terpicu
    deduction = 0.0
    for alert in rule_alerts:
        if "Extreme Power Load" in alert:
            deduction += 25.0
        elif "Voltage Sag" in alert:
            deduction += 30.0

    score = max(0.0, min(100.0, base_score - deduction))

    logger.info("Efficiency score calculated: %.2f (base: %.2f, deductions: %.2f)", score, base_score, deduction)
    return float(round(score, 2))

