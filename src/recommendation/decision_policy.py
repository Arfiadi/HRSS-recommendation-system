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

    # Pemetaan Tingkat Inefisiensi
    if not switch_recommended and len(rule_alerts) == 0:
        risk_level = "Optimal Efficiency"
        primary_recommendation = (
            f"Kondisi pergerakan ideal. Pertahankan mesin pada mode {current_mode} untuk efisiensi energi maksimal."
        )

    elif switch_recommended and len(rule_alerts) == 0:
        risk_level = "Sub-optimal Movement"
        primary_recommendation = (
            f"Pola pergerakan terdeteksi kurang efisien. "
            f"Sistem merekomendasikan transisi ke mode {predicted_mode} untuk optimasi lintasan dan penghematan daya."
        )

    else:
        # Jika ada inefisiensi ekstrem dari Rule Engine (misal: daya tinggi tapi minim gerak)
        risk_level = "Critical Inefficiency"
        if current_mode.strip().lower() == "optimized":
            primary_recommendation = (
                "Terdeteksi pemborosan energi tinggi akibat pergerakan tidak wajar. "
                "Sistem menyarankan kembali ke pola pergerakan Standard sementara untuk stabilisasi konsumsi daya."
            )
        else:
            primary_recommendation = (
                "Terdeteksi pemborosan energi tinggi akibat pergerakan tidak wajar. "
                "Sistem menyarankan tetap di pola Standard dan meninjau ulang algoritma routing (WMS)."
            )

    logger.info("Decision generated. Efficiency Status: %s", risk_level)
    return risk_level, primary_recommendation
