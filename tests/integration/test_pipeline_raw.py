"""
Integration Test — Pipeline dengan RAW Features.
"""
import pandas as pd
from src.pipeline.inference_pipeline import run_inference_pipeline


def test_inference_pipeline_raw():
    # Load dataset test dan hapus engineered features untuk menyimulasikan data IoT mentah
    test_df = pd.read_csv("data/splits/X_test.csv")

    # Ambil baris pertama
    sample = test_df.iloc[0].to_dict()
    sample.pop("operation_type", None)

    # Hapus engineered features agar build_features dipanggil
    engineered_cols = [
        "total_power",
        "avg_voltage",
        "active_motor_count",
    ]
    for col in engineered_cols:
        sample.pop(col, None)

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
