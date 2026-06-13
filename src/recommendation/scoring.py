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
    # Base score diasumsikan 100 (Kondisi mesin fisik sempurna)
    base_score = 100.0
    deduction = 0.0

    # 1. Penalti dari Machine Learning (Inefisiensi Rute)
    # probability_optimized = 1.0 -> penalti 0 poin
    # probability_optimized = 0.0 -> penalti 20 poin
    routing_penalty = (1.0 - probability_optimized) * 20.0
    deduction += routing_penalty

    # 2. Penalti dari Rule Engine (Anomali Kelistrikan Fisik)
    for alert in rule_alerts:
        if "Beban Daya Ekstrem" in alert:
            deduction += 15.0
        elif "Tegangan Anjlok" in alert:
            deduction += 25.0

    score = max(0.0, min(100.0, base_score - deduction))

    logger.info("Efficiency score calculated: %.2f (routing penalty: %.2f, total deduction: %.2f)", score, routing_penalty, deduction)
    return float(round(score, 2))

