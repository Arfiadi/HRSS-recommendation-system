from pathlib import Path
import pandas as pd


def load_csv(path, **kwargs):
    return pd.read_csv(Path(path), **kwargs)


def save_csv(df, path, **kwargs):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(Path(path), index=False, **kwargs)
