"""
Response Schemas — Pydantic model untuk format output API.
"""
from pydantic import BaseModel, Field
from typing import List


class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="ID prediksi kelas (0 atau 1)")
    prediction_label: str = Field(..., description="Label prediksi (standard_operation atau optimized_operation)")
    probability_standard: float = Field(..., description="Probabilitas ke arah Standard Operation")
    probability_optimized: float = Field(..., description="Probabilitas ke arah Optimized Operation")


class RecommendationResponse(BaseModel):
    # ML Preds
    prediction: int = Field(..., description="ID prediksi kelas (0 atau 1)")
    prediction_label: str = Field(..., description="Label prediksi")
    probability_standard: float = Field(..., description="Probabilitas ke arah Standard Operation")
    probability_optimized: float = Field(..., description="Probabilitas ke arah Optimized Operation")

    # Recommendation Engine outputs
    current_machine_mode: str = Field(..., description="Mode operasional aktual saat ini")
    ml_predicted_profile: str = Field(..., description="Profil mode hasil rekomendasi AI")
    operational_risk_level: str = Field(..., description="Tingkat risiko operasional sistem")
    primary_recommendation: str = Field(..., description="Rekomendasi utama yang disarankan")
    technical_alerts: List[str] = Field(..., description="Daftar alert/peringatan teknis spesifik")
    efficiency_score: float = Field(..., description="Skor efisiensi operasional akhir (0-100)")
