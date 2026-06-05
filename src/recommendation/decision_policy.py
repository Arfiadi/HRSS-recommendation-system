"""
Decision Policy — Kebijakan keputusan berdasarkan risiko operasional.

Menggabungkan hasil model ML + rule engine menjadi keputusan final.
"""
import logging

logger = logging.getLogger(__name__)


def generate_decision(
    current_mode: str,
    predicted_mode: str,
    probability_optimized: float,
    rule_alerts: list,
) -> tuple:
    """
    Menggabungkan probabilitas ML, status mesin, dan Rules menjadi Rekomendasi Preskriptif.

    Args:
        current_mode: Mode mesin saat ini ('Standard' atau 'Optimized').
        predicted_mode: Profil operasional yang diprediksi ML ('Standard' atau 'Optimized').
        probability_optimized: Nilai probabilitas ke arah Optimized (0.0 - 1.0).
        rule_alerts: Daftar alert yang terpicu dari Rule Engine.

    Returns:
        Tuple berisi (risk_level, primary_recommendation).
    """
    # Identifikasi selisih kondisi (Switch Logic)
    switch_recommended = current_mode.strip().lower() != predicted_mode.strip().lower()

    # Pemetaan Tingkat Risiko (Risk Level Mapping)
    if not switch_recommended and len(rule_alerts) == 0:
        risk_level = "Low Risk (Normal Operation)"
        primary_recommendation = (
            f"Kondisi beban ideal. Pertahankan mesin pada mode {current_mode}."
        )

    elif switch_recommended and len(rule_alerts) == 0:
        risk_level = "Medium Inefficiency"
        primary_recommendation = (
            f"Pola kelistrikan cocok untuk mode {predicted_mode}. "
            f"Disarankan melakukan transisi mode untuk meningkatkan efisiensi operasional."
        )

    else:
        # Jika ada peringatan mekanis/kelistrikan dari Rule Engine
        risk_level = "High Inefficiency / Mechanical Anomaly"
        if current_mode.strip().lower() == "optimized":
            primary_recommendation = (
                "Terdeteksi anomali beban fisik. Sistem menyarankan beralih ke mode Standard "
                "untuk melindungi motor servo dari panas/aus."
            )
        else:
            primary_recommendation = (
                "Terdeteksi anomali beban fisik. Sistem menyarankan tetap berada di mode Standard "
                "untuk melindungi motor servo dari panas/aus."
            )

    logger.info("Decision generated. Risk Level: %s", risk_level)
    return risk_level, primary_recommendation
