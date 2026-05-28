import numpy as np
import mlflow

from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    recall_score,
    precision_score,
    confusion_matrix
)


# =========================================================
# CORE EVALUATION FUNCTION
# =========================================================

def evaluate_model(y_true, y_pred, y_proba=None):
    """
    Industrial-grade evaluation function for binary classification:
    0 = standard operation
    1 = optimized operation
    """

    # Confusion Matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    # =====================================================
    # PRIMARY METRICS
    # =====================================================
    f1_macro = f1_score(y_true, y_pred, average='macro')

    roc_auc = None
    if y_proba is not None:
        roc_auc = roc_auc_score(y_true, y_proba)

    # =====================================================
    # SECONDARY METRICS
    # =====================================================
    recall_class_1 = recall_score(y_true, y_pred, pos_label=1)
    precision_class_1 = precision_score(y_true, y_pred, pos_label=1)

    # =====================================================
    # RISK METRICS
    # =====================================================
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

    return {
        # PRIMARY
        "f1_macro": f1_macro,
        "roc_auc": roc_auc,

        # SECONDARY
        "recall_class_1": recall_class_1,
        "precision_class_1": precision_class_1,

        # RISK
        "fpr": fpr,
        "fnr": fnr,

        # RAW CONFUSION MATRIX
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }


# =========================================================
# MLFLOW LOGGER
# =========================================================

def log_metrics_mlflow(metrics: dict):
    """
    Log evaluation metrics into MLflow in standardized format.
    """

    mlflow.log_metric("f1_macro", metrics["f1_macro"])
    mlflow.log_metric("roc_auc", metrics["roc_auc"] if metrics["roc_auc"] is not None else 0)

    mlflow.log_metric("recall_class_1", metrics["recall_class_1"])
    mlflow.log_metric("precision_class_1", metrics["precision_class_1"])

    mlflow.log_metric("fpr", metrics["fpr"])
    mlflow.log_metric("fnr", metrics["fnr"])


# =========================================================
# HUMAN-READABLE REPORT
# =========================================================

def print_evaluation_report(metrics: dict):
    """
    Print clean evaluation summary for notebook analysis.
    """

    print("\n==============================")
    print("INDUSTRIAL MODEL EVALUATION")
    print("==============================")

    print(f"F1 Macro            : {metrics['f1_macro']:.4f}")
    print(f"ROC AUC             : {metrics['roc_auc']:.4f}")

    print("\n--- Secondary Metrics ---")
    print(f"Recall Class 1     : {metrics['recall_class_1']:.4f}")
    print(f"Precision Class 1  : {metrics['precision_class_1']:.4f}")

    print("\n--- Risk Metrics ---")
    print(f"False Positive Rate : {metrics['fpr']:.4f}")
    print(f"False Negative Rate : {metrics['fnr']:.4f}")

    print("\n--- Confusion Matrix ---")
    print(f"TP: {metrics['tp']} | FP: {metrics['fp']}")
    print(f"FN: {metrics['fn']} | TN: {metrics['tn']}")

    print("==============================\n")


# =========================================================
# BATCH EVALUATION (OPTIONAL BUT USEFUL)
# =========================================================

def evaluate_batch(models_dict, X_test, y_test):
    """
    Evaluate multiple models in one go.
    
    Args:
        models_dict: {"model_name": trained_model}
    """

    results = {}

    for name, model in models_dict.items():

        y_pred = model.predict(X_test)

        y_proba = None
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]

        metrics = evaluate_model(y_test, y_pred, y_proba)

        results[name] = metrics

    return results