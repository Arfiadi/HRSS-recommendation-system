"""
Integration Test — FastAPI endpoints (health, predict, recommend).
"""
import pandas as pd
from fastapi.testclient import TestClient
from src.api.main import app


def test_api_endpoints():
    # Gunakan TestClient untuk menguji server FastAPI secara in-process
    with TestClient(app) as client:
        # 1. Test Health Check
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        # Load sample data dari X_test.csv
        test_df = pd.read_csv("data/splits/X_test.csv")
        sample = test_df.iloc[0].to_dict()
        sample.pop("operation_type", None)

        # Hapus engineered features untuk menyimulasikan data sensor IoT mentah
        engineered_cols = [
            "total_power",
            "avg_voltage",
            "total_movement",
            "power_efficiency_ratio",
            "rail_activity",
            "conveyor_activity",
        ]
        for col in engineered_cols:
            sample.pop(col, None)

        # 2. Test Predict Route
        sample["Timestamp"] = 0.0
        pred_response = client.post("/api/v1/predict", json=sample)
        assert pred_response.status_code == 200
        pred_json = pred_response.json()
        assert "prediction" in pred_json
        assert "prediction_label" in pred_json
        assert "probability_standard" in pred_json
        assert "probability_optimized" in pred_json

        # 3. Test Recommend Route
        payload = {"telemetry": sample, "current_mode": "Standard"}
        rec_response = client.post("/api/v1/recommend", json=payload)
        assert rec_response.status_code == 200
        rec_json = rec_response.json()

        assert "prediction" in rec_json
        assert "prediction_label" in rec_json
        assert "current_machine_mode" in rec_json
        assert rec_json["current_machine_mode"] == "Standard"
        assert "ml_predicted_profile" in rec_json
        assert "operational_risk_level" in rec_json
        assert "primary_recommendation" in rec_json
        assert "technical_alerts" in rec_json
        assert isinstance(rec_json["technical_alerts"], list)
        assert "efficiency_score" in rec_json
        assert 0.0 <= rec_json["efficiency_score"] <= 100.0
