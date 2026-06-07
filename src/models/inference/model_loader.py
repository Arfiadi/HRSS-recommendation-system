"""
Model Loader — Memuat model ML yang sudah terlatih dari storage.

Mendukung loading dari file .pkl lokal maupun dari MLflow Model Registry.
Termasuk caching agar model tidak perlu di-load ulang setiap request API.
"""
import pickle
import logging

logger = logging.getLogger(__name__)

# In-memory cache
_model_cache = {}


def load_model_from_pkl(model_path: str):
    """Memuat model dari file .pkl."""
    if model_path in _model_cache:
        logger.info("Model loaded from cache: %s", model_path)
        return _model_cache[model_path]

    logger.info("Loading model from pkl: %s", model_path)
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    _model_cache[model_path] = model
    return model


def clear_cache():
    """Membersihkan cache model dari memori."""
    _model_cache.clear()
    logger.info("Model cache cleared.")
