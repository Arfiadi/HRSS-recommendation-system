"""
Model Validation — Validasi model sebelum deployment.

Mengecek apakah model memenuhi success criteria dan
tidak menunjukkan tanda-tanda overfitting.
"""
import logging

from src.core.problem_definition import SUCCESS_CRITERIA

logger = logging.getLogger(__name__)


def validate_model_performance(metrics: dict, criteria: dict = None) -> bool:
    """
    Mengecek apakah metrik model memenuhi threshold minimum:
    f1_macro >= 0.85, roc_auc >= 0.90, dll.

    Returns:
        True jika model memenuhi semua kriteria, False jika tidak.
    """
    if criteria is None:
        criteria = SUCCESS_CRITERIA

    passed = True

    if metrics["f1_macro"] < criteria["f1_macro_min"]:
        logger.warning(
            "FAIL: f1_macro %.4f < threshold %.4f",
            metrics["f1_macro"], criteria["f1_macro_min"],
        )
        passed = False

    if metrics["roc_auc"] is not None and metrics["roc_auc"] < criteria["roc_auc_min"]:
        logger.warning(
            "FAIL: roc_auc %.4f < threshold %.4f",
            metrics["roc_auc"], criteria["roc_auc_min"],
        )
        passed = False

    if passed:
        logger.info("Model validation PASSED all success criteria.")
    else:
        logger.error("Model validation FAILED. Review metrics before deployment.")

    return passed


def check_overfitting(train_metrics: dict, test_metrics: dict, max_gap: float = 0.05) -> bool:
    """
    Mengecek apakah ada indikasi overfitting berdasarkan gap
    antara metrik train dan test.

    Returns:
        True jika TIDAK overfitting, False jika terdeteksi.
    """
    gap = abs(train_metrics["f1_macro"] - test_metrics["f1_macro"])

    if gap > max_gap:
        logger.warning(
            "OVERFITTING WARNING: F1 gap = %.4f (train: %.4f, test: %.4f, max: %.4f)",
            gap, train_metrics["f1_macro"], test_metrics["f1_macro"], max_gap,
        )
        return False

    logger.info("Overfitting check PASSED. F1 gap: %.4f", gap)
    return True
