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
    # Default values
    risk_level = "Optimal Efficiency"
    primary_recommendation = "Kondisi pergerakan ideal. Pertahankan konfigurasi saat ini."

    current = current_mode.strip().lower()
    predicted = predicted_mode.strip().lower()

    if len(rule_alerts) == 0:
        if current == "standard" and predicted == "standard":
            risk_level = "Sub-optimal Movement"
            primary_recommendation = (
                "Sistem beroperasi pada rute Standard (Non-Optimized). "
                "Sistem merekomendasikan transisi ke mode Optimized (Smart Routing) pada WMS "
                "untuk memperpendek lintasan dan menghemat daya."
            )
        elif current == "standard" and predicted == "optimized":
            risk_level = "Optimal Efficiency"
            primary_recommendation = (
                "Meskipun disetel ke Standard, pola pergerakan saat ini sangat efisien menyerupai mode Optimized. "
                "Pertahankan performa ini atau lakukan transisi penuh ke mode Optimized."
            )
        elif current == "optimized" and predicted == "standard":
            risk_level = "Sub-optimal Movement"
            primary_recommendation = (
                "Mesin disetel ke mode Optimized, namun pola pergerakan terdeteksi kurang efisien "
                "(menyerupai rute panjang Standard). Periksa kembali algoritma WMS Anda, "
                "optimasi lintasan tampaknya tidak berjalan semestinya."
            )
        elif current == "optimized" and predicted == "optimized":
            risk_level = "Optimal Efficiency"
            primary_recommendation = (
                "Smart Routing berjalan sempurna. Konsumsi daya dan rute pergerakan sangat efisien. "
                "Pertahankan mode Optimized."
            )
    else:
        # Ada alert dari Rule Engine (Critical)
        risk_level = "Critical Inefficiency"
        if current == "optimized":
            primary_recommendation = (
                "Terdeteksi beban daya ekstrem atau anjloknya tegangan! "
                "Mode Optimized (Smart Routing) mungkin terlalu agresif membebani motor rel. "
                "Sistem menyarankan kembali ke mode Standard sementara untuk menstabilkan kelistrikan."
            )
        else:
            primary_recommendation = (
                "Terdeteksi beban daya ekstrem atau anjloknya tegangan pada mode Standard. "
                "Kurangi beban operasional secara manual atau jadwalkan inspeksi kelistrikan motor."
            )

    logger.info("Decision generated. Efficiency Status: %s", risk_level)
    return risk_level, primary_recommendation
