"""
Prediction Service — Reusable logic untuk prediksi ML.

File ini membungkus logika prediksi yang memuat model ML
dan memprediksi output probabilitas.
"""
import pandas as pd
import logging
from src.models.inference.model_loader import load_model_from_pkl
from src.models.inference.predictor import predict_with_probability
from src.core.problem_definition import MODEL_FEATURE_COLUMNS, ENGINEERED_FEATURES
from src.data.feature_engineering import build_features
from src.features.feature_validator import validate_features

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(
        self,
        model_path: str = "models/final_hrss_rf_model.pkl",
    ):
        """
        Inisialisasi Prediction Service.

        Args:
            model_path: Path ke file .pkl model.
        """
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """Memuat model secara otomatis dari path lokal."""
        try:
            logger.info("PredictionService: Loading model from path %s", self.model_path)
            self.model = load_model_from_pkl(self.model_path)
            logger.info("PredictionService: Model successfully loaded.")
        except Exception as e:
            logger.error("PredictionService: Failed to load model: %s", str(e))
            raise e

    def preprocess(self, raw_input: dict) -> pd.DataFrame:
        """
        Preprocess raw input menjadi feature DataFrame.

        Args:
            raw_input: Telemetry input data sensor.

        Returns:
            Pandas DataFrame hasil feature engineering.
        """
        df = pd.DataFrame([raw_input])
        # Cek jika input sudah ter-feature engineered (harus ada kolomnya dan tidak bernilai null)
        has_engineered = all(feat in df.columns for feat in ENGINEERED_FEATURES) and not df[ENGINEERED_FEATURES].isnull().any().any()
        if not has_engineered:
            logger.debug("PredictionService: Running feature engineering on raw inputs...")
            df = build_features(df)
        else:
            logger.debug("PredictionService: Engineered features already present, skipping build.")
        return df

    def predict(self, raw_input: dict) -> dict:
        """
        Menjalankan preprocessing, validasi fitur, dan estimasi probabilitas model.

        Args:
            raw_input: Dictionary data sensor.

        Returns:
            Dictionary berisi label prediksi dan probabilitas.
        """
        df = self.preprocess(raw_input)
        if not validate_features(df, MODEL_FEATURE_COLUMNS):
            raise ValueError("Feature validation failed. Missing or null features.")

        features_df = df[MODEL_FEATURE_COLUMNS]
        result = predict_with_probability(self.model, features_df)
        return result
