"""
Inference Pipeline — Orchestration alur prediksi end-to-end.

Menerima data sensor mentah (dict/JSON), menjalankan feature engineering
jika diperlukan, load model, dan mengembalikan hasil prediksi terstruktur.

Usage:
    from src.pipeline.inference_pipeline import run_inference_pipeline
    result = run_inference_pipeline(sensor_data_dict)
"""
import pandas as pd
import logging

from src.data.feature_engineering import build_features
from src.features.feature_validator import validate_features
from src.models.inference.model_loader import load_model_from_pkl
from src.models.inference.predictor import predict_with_probability
from src.core.problem_definition import MODEL_FEATURE_COLUMNS, ENGINEERED_FEATURES

logger = logging.getLogger(__name__)


def run_inference_pipeline(
    input_data: dict,
    model_path: str = "models/final_hrss_rf_model.pkl",
) -> dict:
    """
    Menjalankan seluruh alur inference dari input mentah
    hingga output prediksi terstruktur.

    Args:
        input_data: Dictionary berisi data sensor satu baris
                    (sama persis dengan format yang dikirim IoT/API).
        model_path: Path ke file .pkl model.

    Returns:
        Dictionary berisi prediksi, probabilitas, dan label.
    """
    # Step 1: Convert dict ke DataFrame
    df = pd.DataFrame([input_data])
    logger.info("Inference input received. Columns: %d", len(df.columns))

    # Step 2: Feature Engineering (hanya jika belum ada engineered features)
    has_engineered = all(feat in df.columns for feat in ENGINEERED_FEATURES) and not df[ENGINEERED_FEATURES].isnull().any().any()
    if not has_engineered:
        logger.info("Engineered features not found. Running feature engineering...")
        df = build_features(df)
    else:
        logger.info("Engineered features already present. Skipping feature engineering.")

    # Step 3: Validasi fitur
    if not validate_features(df, MODEL_FEATURE_COLUMNS):
        logger.error("Feature validation failed. Aborting inference.")
        return {"error": "Feature validation failed. Missing or null features."}

    # Step 4: Load model
    if not model_path:
        raise ValueError("model_path must be provided.")
    model = load_model_from_pkl(model_path)

    # Step 5: Predict (gunakan hanya kolom yang diharapkan model, dalam urutan benar)
    features_df = df[MODEL_FEATURE_COLUMNS]
    result = predict_with_probability(model, features_df)

    logger.info("Inference pipeline complete: %s", result["prediction_label"])
    return result
