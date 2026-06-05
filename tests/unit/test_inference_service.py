"""
Unit Test — Inference Service Module.
"""
import pandas as pd
from src.services.inference_service import InferenceService


def test_run_inference_offline():
    # Load InferenceService menggunakan local pkl model
    service = InferenceService(model_path="models/final_hrss_rf_model.pkl")

    # Siapkan data normal satu baris
    test_df = pd.read_csv("data/splits/X_test.csv")
    sample_normal = test_df.iloc[0].to_dict()
    sample_normal.pop("operation_type", None)

    # Jalankan inference
    result = service.run_inference(sample_normal, current_mode="Standard")

    # Pastikan format output benar
    assert "prediction" in result
    assert result["prediction"] in [0, 1]
    assert "prediction_label" in result
    assert "probability_standard" in result
    assert "probability_optimized" in result
    assert 0.0 <= result["probability_standard"] <= 1.0
    assert 0.0 <= result["probability_optimized"] <= 1.0

    assert "current_machine_mode" in result
    assert "ml_predicted_profile" in result
    assert "operational_risk_level" in result
    assert "primary_recommendation" in result
    assert "technical_alerts" in result
    assert isinstance(result["technical_alerts"], list)
    assert "efficiency_score" in result
    assert 0.0 <= result["efficiency_score"] <= 100.0
