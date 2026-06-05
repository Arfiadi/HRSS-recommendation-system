"""
Model Evaluation Plots — Modul untuk visualisasi performa model ML.

Menyediakan fungsi untuk membuat plot Confusion Matrix dan Learning Curve,
serta menyimpannya secara lokal sebagai gambar.
"""
import os
import logging
import numpy as np
import matplotlib
# Gunakan backend non-interaktif agar aman dijalankan di server headless/CI-CD
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import learning_curve

logger = logging.getLogger(__name__)


def plot_confusion_matrix(
    y_true,
    y_pred,
    labels=None,
    output_path: str = None,
) -> plt.Figure:
    """
    Membuat plot Confusion Matrix yang informatif dan menarik menggunakan Seaborn.

    Args:
        y_true: Nilai target aktual.
        y_pred: Nilai prediksi model.
        labels: Label kelas untuk sumbu X dan Y.
        output_path: Path tujuan penyimpanan file gambar (opsional).

    Returns:
        Matplotlib Figure object.
    """
    logger.info("Generating Confusion Matrix plot...")
    
    # Hitung confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Setup visual style
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=True,
        xticklabels=labels if labels else ["Standard", "Optimized"],
        yticklabels=labels if labels else ["Standard", "Optimized"],
        annot_kws={"size": 12, "weight": "bold"},
    )
    
    plt.title("Confusion Matrix", fontsize=14, pad=15)
    plt.ylabel("Actual Label", fontsize=12, labelpad=10)
    plt.xlabel("Predicted Label", fontsize=12, labelpad=10)
    plt.tight_layout()
    
    fig = plt.gcf()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info("Confusion Matrix plot saved to %s", output_path)
        
    return fig


def plot_learning_curve(
    estimator,
    X,
    y,
    cv: int = 5,
    train_sizes=None,
    output_path: str = None,
    scoring: str = "f1_macro",
) -> plt.Figure:
    """
    Menghitung dan menggambar Learning Curve untuk mendeteksi overfitting/underfitting.

    Args:
        estimator: Estimator / Model Scikit-learn.
        X: Fitur dataset training.
        y: Target dataset training.
        cv: Fold cross-validation.
        train_sizes: Fraksi ukuran training set (default: 5 interval dari 10% ke 100%).
        output_path: Path tujuan penyimpanan file gambar (opsional).
        scoring: Metrik evaluasi yang dihitung (default: 'f1_macro').

    Returns:
        Matplotlib Figure object.
    """
    logger.info("Calculating Learning Curve metrics...")
    
    if train_sizes is None:
        train_sizes = np.linspace(0.1, 1.0, 5)
        
    train_sizes_abs, train_scores, test_scores = learning_curve(
        estimator,
        X,
        y,
        cv=cv,
        train_sizes=train_sizes,
        scoring=scoring,
        n_jobs=-1,
        random_state=42,
    )
    
    # Hitung rata-rata dan standar deviasi
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    
    # Setup visual style
    plt.figure(figsize=(8, 5))
    plt.grid(True, linestyle="--", alpha=0.7)
    
    # Gambar pita standar deviasi (variansi)
    plt.fill_between(
        train_sizes_abs,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.15,
        color="#e74c3c",
    )
    plt.fill_between(
        train_sizes_abs,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.15,
        color="#2ecc71",
    )
    
    # Gambar garis nilai rata-rata
    plt.plot(
        train_sizes_abs,
        train_scores_mean,
        "o-",
        color="#e74c3c",
        linewidth=2,
        label="Training Score",
    )
    plt.plot(
        train_sizes_abs,
        test_scores_mean,
        "o-",
        color="#2ecc71",
        linewidth=2,
        label="Cross-Validation Score",
    )
    
    plt.title(f"Learning Curve ({scoring.replace('_', ' ').title()})", fontsize=14, pad=15)
    plt.xlabel("Training Examples", fontsize=12, labelpad=10)
    plt.ylabel(scoring.replace('_', ' ').title(), fontsize=12, labelpad=10)
    plt.legend(loc="best", fontsize=10)
    plt.tight_layout()
    
    fig = plt.gcf()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info("Learning Curve plot saved to %s", output_path)
        
    return fig
