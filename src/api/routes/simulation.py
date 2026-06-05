"""
Simulation Endpoint — Menyediakan data telemetry riil dari dataset training untuk simulasi frontend.
"""
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os
import time

router = APIRouter()

# Global cache untuk dataset agar tidak read file setiap request
_datasets = {}

def get_dataset(scenario: str) -> pd.DataFrame:
    if scenario not in _datasets:
        if scenario.lower() == "optimized":
            path = "data/raw/HRSS_normal_optimized.csv"
        else:
            path = "data/raw/HRSS_normal_standard.csv"
            
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Dataset file not found at {path}")
            
        df = pd.read_csv(path)
        # Drop operation_type dan Labels jika ada agar bersih
        df = df.drop(columns=["operation_type", "Labels"], errors="ignore")
        _datasets[scenario] = df
        
    return _datasets[scenario]

@router.get("/simulate/telemetry", tags=["Simulation"])
def get_simulated_telemetry(
    scenario: str = Query("Standard", description="Scenario type: Standard or Optimized"),
    index: int = Query(0, description="Index of the row to retrieve")
):
    try:
        df = get_dataset(scenario)
        row_idx = index % len(df)
        row_dict = df.iloc[row_idx].to_dict()
        
        # Override Timestamp dengan timestamp aktual agar real-time di chart
        row_dict["Timestamp"] = time.time()
        
        return row_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
