import pandas as pd
import glob
from src.data.feature_engineering import build_features

def test_data_context_2():
    csv_files = glob.glob("data/raw/*.csv")
    dfs = []
    for f in csv_files:
        dfs.append(pd.read_csv(f))
    df = pd.concat(dfs, ignore_index=True)
    df = build_features(df)
    
    print("\n--- Statistics of Engineered Features ---")
    print("total_power:")
    print(df["total_power"].describe())
    
    print("\ntotal_movement:")
    print(df["total_movement"].describe())

    print("\npower_efficiency_ratio:")
    print(df["power_efficiency_ratio"].describe())
    
    print("\navg_voltage:")
    print(df["avg_voltage"].describe())
    
    print("\nrail_activity:")
    print(df["rail_activity"].describe())

if __name__ == "__main__":
    test_data_context_2()
