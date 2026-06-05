"""
MLflow Configuration — Setup dan utilitas MLflow tracking.

Menyediakan fungsi setup experiment, logging run,
dan utilitas perbandingan antar run.
"""
import mlflow
import mlflow.sklearn
import logging

logger = logging.getLogger(__name__)


def setup_mlflow(tracking_uri: str, experiment_name: str):
    """Setup MLflow tracking URI dan experiment."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    logger.info(
        "MLflow configured — URI: %s, Experiment: %s",
        tracking_uri, experiment_name,
    )


def log_experiment_run(model, metrics: dict, params: dict, model_name: str = "hrss_model"):
    """
    Log satu run experiment ke MLflow.

    Logs parameters, metrics, dan model artifact secara otomatis.
    """
    mlflow.log_params(params)
    mlflow.log_metrics({k: v for k, v in metrics.items() if v is not None})
    mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=model_name)
    logger.info("MLflow run logged successfully with %d metrics.", len(metrics))
