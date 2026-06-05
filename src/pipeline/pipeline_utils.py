"""
Pipeline Utilities — Fungsi pembantu untuk orchestration pipeline.

Menyediakan config loader, step logger, dan validasi antar step.
"""
import os
import time
import yaml
import logging

logger = logging.getLogger(__name__)


def load_pipeline_config(config_path: str = "configs/config.yaml") -> dict:
    """Memuat konfigurasi pipeline dari file YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info("Pipeline config loaded from: %s", config_path)
    return config


def log_step(step_name: str, status: str, duration: float = None):
    """Mencatat log eksekusi step pipeline."""
    msg = f"[PIPELINE] Step '{step_name}' — {status}"
    if duration is not None:
        msg += f" (duration: {duration:.2f}s)"
    logger.info(msg)


class StepTimer:
    """Context manager untuk mengukur durasi step pipeline."""

    def __init__(self, step_name: str):
        self.step_name = step_name
        self.start = None
        self.duration = None

    def __enter__(self):
        self.start = time.time()
        log_step(self.step_name, "STARTED")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start
        status = "COMPLETED" if exc_type is None else f"FAILED ({exc_type.__name__})"
        log_step(self.step_name, status, self.duration)
        return False  # don't suppress exceptions
