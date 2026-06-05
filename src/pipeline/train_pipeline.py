"""
Training Pipeline — Orchestration alur training end-to-end.

Skrip ini adalah ORKESTRATOR yang mengatur urutan pemanggilan
modul-modul lain untuk proses training dari data mentah hingga
model terdaftar di MLflow registry.

Usage:
    python -m src.pipeline.train_pipeline
"""
import os
import sys
import logging
import mlflow

from src.pipeline.pipeline_utils import load_pipeline_config, StepTimer
from src.data.ingestion import load_raw_datasets, validate_raw_data
from src.data.preprocessing import clean_data
from src.data.feature_engineering import build_features
from src.data.split import create_and_save_splits
from src.models.training.train_pipeline import train_random_forest
from src.evaluation.evaluator import evaluate_and_report
from src.evaluation.metrics import log_metrics_mlflow
from src.evaluation.validation import validate_model_performance
from src.evaluation.plots import plot_confusion_matrix, plot_learning_curve
from src.tracking.mlflow_config import setup_mlflow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def run_training_pipeline(config_path: str = "configs/config.yaml"):
    """
    Menjalankan seluruh alur training dari data mentah
    hingga model terdaftar di MLflow registry.
    """
    # --- Load Config ---
    config = load_pipeline_config(config_path)
    seed = config["project"]["random_seed"]

    # --- Setup MLflow ---
    setup_mlflow(
        tracking_uri=config["mlflow"]["tracking_uri"],
        experiment_name=config["mlflow"]["experiment_name"],
    )

    with mlflow.start_run(run_name="production_training_v1") as run:
        # Step 1: Data Ingestion
        with StepTimer("Data Ingestion"):
            raw_df = load_raw_datasets(config["paths"]["raw_data"])
            assert validate_raw_data(raw_df), "Raw data validation failed!"

        # Step 2: Data Preprocessing
        with StepTimer("Data Preprocessing"):
            clean_df = clean_data(raw_df)

        # Step 3: Feature Engineering
        with StepTimer("Feature Engineering"):
            featured_df = build_features(clean_df)

        # Step 4: Train/Test Split
        with StepTimer("Train/Test Split"):
            X_train, X_test, y_train, y_test = create_and_save_splits(
                featured_df,
                splits_dir=config["paths"]["splits"],
                test_size=config["training"]["test_size"],
                seed=seed,
            )

        # Step 5: Model Training
        with StepTimer("Model Training"):
            model = train_random_forest(
                X_train, y_train,
                n_estimators=config["training"]["n_estimators"],
                random_state=seed,
            )

        # Step 6: Model Evaluation
        with StepTimer("Model Evaluation"):
            metrics = evaluate_and_report(model, X_test, y_test)
            
            # Generate Evaluation Plots
            figures_dir = config["paths"]["figures"]
            cm_path = os.path.join(figures_dir, "confusion_matrix.png")
            lc_path = os.path.join(figures_dir, "learning_curve.png")
            plot_confusion_matrix(y_test, model.predict(X_test), output_path=cm_path)
            plot_learning_curve(model, X_train, y_train, output_path=lc_path)

        # Step 7: Log to MLflow
        with StepTimer("MLflow Logging"):
            params = {
                "model_type": config["training"]["model_type"],
                "n_estimators": config["training"]["n_estimators"],
                "test_size": config["training"]["test_size"],
                "random_seed": seed,
                "n_features": X_train.shape[1],
                "n_train_samples": X_train.shape[0],
            }
            log_metrics_mlflow(metrics)
            mlflow.log_params(params)
            
            # Log plots as artifacts
            mlflow.log_artifact(cm_path, artifact_path="plots")
            mlflow.log_artifact(lc_path, artifact_path="plots")
            
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                registered_model_name="hrss_model",
            )

        # Step 8: Validate Before Deployment
        with StepTimer("Model Validation"):
            is_valid = validate_model_performance(metrics)

        # --- Summary ---
        logger.info("=" * 60)
        logger.info("TRAINING PIPELINE COMPLETE")
        logger.info("MLflow Run ID: %s", run.info.run_id)
        logger.info("Model valid for deployment: %s", is_valid)
        logger.info("=" * 60)

        return {
            "run_id": run.info.run_id,
            "metrics": metrics,
            "is_valid": is_valid,
        }


if __name__ == "__main__":
    run_training_pipeline()
