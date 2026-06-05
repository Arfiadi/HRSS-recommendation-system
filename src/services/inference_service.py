"""
Inference Service — Unified entry point untuk seluruh proses inference.

File ini adalah FACADE (pintu utama) yang menyatukan prediction_service
dan recommendation_service menjadi satu interface yang mudah dipanggil.
"""
import logging
from src.services.prediction_service import PredictionService
from src.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(
        self,
        model_path: str = "models/final_hrss_rf_model.pkl",
    ):
        """
        Inisialisasi unified Inference Service.

        Args:
            model_path: Path lokal model file (.pkl).
        """
        self.prediction_service = PredictionService(
            model_path=model_path,
        )
        self.recommendation_service = RecommendationService()

    def run_inference(self, input_data: dict, current_mode: str = "Standard") -> dict:
        """
        Menjalankan pipeline utuh: preprocessing -> prediction -> recommendation.

        Args:
            input_data: Data telemetry raw dari sensor (IoT/API).
            current_mode: Mode mesin aktual saat ini ('Standard' atau 'Optimized').

        Returns:
            Dictionary gabungan hasil prediksi ML dan rekomendasi hybrid.
        """
        logger.info("InferenceService: Running end-to-end inference flow...")

        # 1. Preprocess & Predict
        telemetry_df = self.prediction_service.preprocess(input_data)
        pred_result = self.prediction_service.predict(input_data)

        # 2. Recommendation
        rec_result = self.recommendation_service.generate(
            prediction_result=pred_result,
            telemetry_df=telemetry_df,
            current_mode=current_mode,
        )

        # Gabungkan output hasil ML dan Decision Policy
        combined_result = {**pred_result, **rec_result}
        logger.info("InferenceService: End-to-end inference flow complete.")
        return combined_result
