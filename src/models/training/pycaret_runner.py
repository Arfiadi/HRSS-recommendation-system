"""
PyCaret Runner — DEPRECATED for production use.

PyCaret digunakan pada fase eksperimen (Notebook 03) untuk
membandingkan banyak model secara cepat. Pada production,
kita menggunakan sklearn RandomForestClassifier secara langsung
melalui src.models.training.train_pipeline.

File ini dipertahankan sebagai referensi dan cadangan apabila
di masa depan dibutuhkan eksperimen ulang via skrip.
"""
import logging

logger = logging.getLogger(__name__)


def train_with_pycaret(train_df, target_col, experiment_name):
    """
    Setup PyCaret, compare models, tune best model, save artifact.

    NOTE: Gunakan hanya untuk eksperimen cepat.
    Untuk production training, gunakan src.pipeline.train_pipeline.
    """
    try:
        from pycaret.classification import ClassificationExperiment
    except ImportError:
        logger.error("PyCaret is not installed. Install with: pip install pycaret")
        raise

    exp = ClassificationExperiment()
    exp.setup(
        data=train_df,
        target=target_col,
        session_id=42,
        experiment_name=experiment_name,
        log_experiment=True,
    )

    best_model = exp.compare_models(fold=5, sort="F1")
    logger.info("PyCaret best model: %s", type(best_model).__name__)

    return best_model
