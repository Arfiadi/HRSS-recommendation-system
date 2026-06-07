"""
Predictor — Menjalankan prediksi menggunakan model ML yang sudah dimuat.

Menyediakan fungsi predict dan predict_with_probability yang
menerima DataFrame fitur dan mengembalikan hasil prediksi terstruktur.
"""
import pandas as pd
import numpy as np
import logging

from src.core.problem_definition import CLASS_LABELS

logger = logging.getLogger(__name__)


def predict(model, features: pd.DataFrame) -> np.ndarray:
    """Menjalankan model.predict() dan mengembalikan array prediksi."""
    predictions = model.predict(features)
    logger.info("Prediction complete. %d samples processed.", len(predictions))
    return predictions


def predict_with_probability(model, features: pd.DataFrame) -> dict:
    """
    Mengembalikan prediksi beserta probabilitasnya.

    Returns:
        {
            "prediction": 1,
            "prediction_label": "optimized_operation",
            "probability_standard": 0.13,
            "probability_optimized": 0.87,
        }
    """
    # Pastikan urutan kolom sama persis dengan saat training
    if hasattr(model, "feature_names_in_"):
        features = features[list(model.feature_names_in_)]

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    result = {
        "prediction": int(pred),
        "prediction_label": CLASS_LABELS[int(pred)],
        "probability_standard": float(proba[0]),
        "probability_optimized": float(proba[1]),
    }

    logger.info(
        "Prediction: %s (%.2f%% confidence)",
        result["prediction_label"],
        max(proba) * 100,
    )
    return result
