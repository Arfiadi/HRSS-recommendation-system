"""
Integration Test — Pipeline dengan Engineered Features.
"""
import pandas as pd
from src.pipeline.inference_pipeline import run_inference_pipeline


def test_inference_pipeline_engineered():
    # Load dataset test yang sudah berisi engineered features
    test_df = pd.read_csv("data/splits/X_test.csv")

    # Ambil baris pertama
    sample = test_df.iloc[0].to_dict()
    sample.pop("operation_type", None)

    # Pastikan engineered features ada di sample
    assert "total_power" in sample
    assert "avg_voltage" in sample

    # Jalankan inference pipeline
    result = run_inference_pipeline(
        sample, model_path="models/final_hrss_rf_model.pkl"
    )

    # Verifikasi hasil
    assert "prediction" in result
    assert result["prediction"] in [0, 1]
    assert "prediction_label" in result
    assert "probability_standard" in result
    assert "probability_optimized" in result
