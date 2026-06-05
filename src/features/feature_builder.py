"""
Feature Builder — Abstraksi pembuatan fitur yang terstruktur.

Membungkus proses feature engineering menjadi sklearn-compatible
Transformer yang bisa dimasukkan ke dalam Pipeline.
"""
import pandas as pd
import logging
from sklearn.base import BaseEstimator, TransformerMixin

from src.data.feature_engineering import build_features

logger = logging.getLogger(__name__)


class FeatureBuilder(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer yang menjalankan
    feature engineering HRSS.

    Dapat digunakan di dalam sklearn.pipeline.Pipeline sehingga
    proses preprocessing & feature engineering terbungkus dalam
    satu objek yang bisa di-serialize bersama model.
    """

    def fit(self, X, y=None):
        """Tidak membutuhkan fitting — transformasi bersifat stateless."""
        return self

    def transform(self, X, y=None):
        """Menjalankan build_features pada DataFrame input."""
        if not isinstance(X, pd.DataFrame):
            raise TypeError("FeatureBuilder expects a pandas DataFrame as input.")

        logger.info("FeatureBuilder transforming data. Input shape: %s", X.shape)
        df = build_features(X)
        logger.info("FeatureBuilder output shape: %s", df.shape)
        return df
