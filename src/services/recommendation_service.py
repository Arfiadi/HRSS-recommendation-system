"""
Recommendation Service — Reusable logic untuk rekomendasi operasional.

File ini membungkus logika rekomendasi yang bisa dipanggil dari mana saja.
Menggabungkan rule_engine + decision_policy + scoring menjadi satu interface.
"""
import pandas as pd
import logging
from src.recommendation.rule_engine import HRSSRuleEngine
from src.recommendation.decision_policy import generate_decision
from src.recommendation.scoring import calculate_efficiency_score

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(self):
        self.rule_engine = HRSSRuleEngine()

    def generate(
        self,
        prediction_result: dict,
        telemetry_df: pd.DataFrame,
        current_mode: str = "Standard",
    ) -> dict:
        """
        Menghasilkan rekomendasi berdasarkan hasil prediksi ML dan telemetry aktual.

        Args:
            prediction_result: Output dictionary dari PredictionService.predict().
            telemetry_df: DataFrame telemetry yang sudah dipreproses.
            current_mode: Mode operasional aktual ('Standard' atau 'Optimized').

        Returns:
            Dictionary berisi keputusan, tingkat risiko, technical alerts, dan skor efisiensi.
        """
        # 1. Evaluasi Domain Rules
        alerts = self.rule_engine.evaluate_rules(telemetry_df)

        # 2. Ekstrak Parameter ML
        prob_optimized = prediction_result["probability_optimized"]
        pred_label = prediction_result["prediction_label"]

        # Konversi nama label ke mode (Standard / Optimized)
        predicted_mode = "Optimized" if "optimized" in pred_label.lower() else "Standard"

        # 3. Decision Policy Layer
        risk_level, primary_recommendation = generate_decision(
            current_mode=current_mode,
            predicted_mode=predicted_mode,
            probability_optimized=prob_optimized,
            rule_alerts=alerts,
        )

        # 4. Hitung Skor Efisiensi
        eff_score = calculate_efficiency_score(telemetry_df, prob_optimized, alerts)

        logger.info("Recommendation successfully generated. Risk Level: %s", risk_level)
        return {
            "current_machine_mode": current_mode,
            "ml_predicted_profile": predicted_mode,
            "probability_optimized": prob_optimized,
            "operational_risk_level": risk_level,
            "primary_recommendation": primary_recommendation,
            "technical_alerts": alerts,
            "efficiency_score": eff_score,
        }
