"""
Export Champion Model — Skrip CI/CD untuk menarik model @champion dari MLflow
dan mengekspornya menjadi file .pkl lokal untuk deployment offline.

Usage:
    python -m src.scripts.export_champion
"""
import os
import shutil
import logging
import pickle
import mlflow
from mlflow.tracking import MlflowClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Konfigurasi default (bisa disesuaikan lewat config.yaml jika perlu)
TRACKING_URI = "sqlite:///mlflow.db"
MODEL_NAME = "hrss_model"
ALIAS_NAME = "champion"
OUTPUT_DIR = "models"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "final_hrss_rf_model.pkl")


def export_champion_model():
    """
    Menghubungkan ke MLflow, mencari model champion, mengunduhnya,
    dan menyimpannya secara lokal.
    """
    # 1. Setup MLflow client
    logger.info("Connecting to MLflow Tracking Server at: %s", TRACKING_URI)
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()

    # Pastikan direktori output ada
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Cari model champion
    logger.info("Searching for model: '%s' with alias: '%s'...", MODEL_NAME, ALIAS_NAME)
    try:
        # Cari versi model berdasarkan alias 'champion'
        model_version_details = client.get_model_version_by_alias(name=MODEL_NAME, alias=ALIAS_NAME)
        version = model_version_details.version
        logger.info("Found champion model version: %s", version)
    except Exception as e:
        logger.warning(
            "Alias '%s' not found for model '%s' in Registry. Details: %s",
            ALIAS_NAME, MODEL_NAME, str(e)
        )
        
        # Fallback: Cari versi terbaru dan setel sebagai champion default
        logger.info("Attempting fallback to latest model version...")
        try:
            versions = client.get_latest_versions(MODEL_NAME)
            if not versions:
                raise ValueError(f"No versions of model '{MODEL_NAME}' found in registry. Have you run the training pipeline?")
            
            latest_version = versions[0].version
            logger.info("Found latest version: %s. Setting alias '%s' on it...", latest_version, ALIAS_NAME)
            
            # Setel alias champion ke versi terbaru tersebut
            client.set_registered_model_alias(
                name=MODEL_NAME,
                alias=ALIAS_NAME,
                version=latest_version
            )
            version = latest_version
        except Exception as ex:
            logger.critical("Failed to find any registered model to export! %s", str(ex))
            return False

    # 3. Load model object
    model_uri = f"models:/{MODEL_NAME}@{ALIAS_NAME}"
    logger.info("Loading model object from URI: %s", model_uri)
    try:
        # Unduh model menggunakan mlflow.sklearn.load_model
        model = mlflow.sklearn.load_model(model_uri)
    except Exception as e:
        logger.critical("Failed to load model from MLflow: %s", str(e))
        return False

    # 4. Save to local .pkl
    logger.info("Exporting model to local path: %s", OUTPUT_FILE)
    try:
        with open(OUTPUT_FILE, "wb") as f:
            pickle.dump(model, f)
        logger.info("SUCCESS: Champion model successfully exported to %s", OUTPUT_FILE)
        return True
    except Exception as e:
        logger.critical("Failed to write .pkl file: %s", str(e))
        return False


if __name__ == "__main__":
    export_champion_model()
