"""
Unit Test — Evaluation Plots Module.
"""
import os
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from src.evaluation.plots import plot_confusion_matrix, plot_learning_curve


def test_plot_confusion_matrix(tmp_path):
    # Data target dummy
    y_true = np.array([0, 1, 0, 1, 0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1, 0, 0, 0, 1])

    cm_path = os.path.join(tmp_path, "confusion_matrix.png")

    fig = plot_confusion_matrix(y_true, y_pred, output_path=cm_path)

    # Verifikasi objek figure berhasil dibuat
    assert fig is not None

    # Verifikasi file gambar berhasil ditulis ke disk
    assert os.path.exists(cm_path)
    assert os.path.getsize(cm_path) > 0


def test_plot_learning_curve(tmp_path):
    # Dataset klasifikasi dummy
    X, y = make_classification(
        n_samples=60,
        n_features=5,
        n_informative=3,
        n_classes=2,
        random_state=42,
    )
    clf = RandomForestClassifier(n_estimators=5, random_state=42)

    lc_path = os.path.join(tmp_path, "learning_curve.png")

    # Menggunakan cv=2 dan 3 interval train_sizes agar sangat cepat berjalan di testing
    fig = plot_learning_curve(
        clf,
        X,
        y,
        cv=2,
        train_sizes=np.linspace(0.5, 1.0, 3),
        output_path=lc_path,
    )

    # Verifikasi objek figure berhasil dibuat
    assert fig is not None

    # Verifikasi file gambar berhasil ditulis ke disk
    assert os.path.exists(lc_path)
    assert os.path.getsize(lc_path) > 0
