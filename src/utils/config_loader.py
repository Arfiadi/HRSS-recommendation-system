from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
MLRUNS_DIR = ROOT / "mlruns"

# Example paths
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

