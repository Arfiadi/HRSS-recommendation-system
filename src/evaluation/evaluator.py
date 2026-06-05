"""
Model Evaluator — Mengevaluasi performa model ML secara komprehensif.

Menggunakan fungsi inti dari src.evaluation.metrics dan menambahkan
lapisan reporting serta visualisasi di atasnya.
"""
import logging
from src.evaluation.metrics import evaluate_model, print_evaluation_report

logger = logging.getLogger(__name__)


def evaluate_and_report(model, X_test, y_test) -> dict:
    """
    Menjalankan evaluasi lengkap: prediksi, hitung metrik, cetak laporan.

    Returns:
        Dictionary berisi semua metrik evaluasi.
    """
    y_pred = model.predict(X_test)

    y_proba = None
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_proba)
    print_evaluation_report(metrics)

    logger.info("Model evaluation complete. F1-macro: %.4f, ROC-AUC: %s",
                metrics["f1_macro"],
                f"{metrics['roc_auc']:.4f}" if metrics["roc_auc"] else "N/A")

    return metrics
