import pandas as pd
import glob
from src.data.feature_engineering import build_features
from src.recommendation.rule_engine import HRSSRuleEngine

def test_data_context():
    csv_files = glob.glob("data/raw/*.csv")
    print(f"Found {len(csv_files)} files: {csv_files}")
    
    dfs = []
    for f in csv_files:
        df_tmp = pd.read_csv(f)
        dfs.append(df_tmp)
        
    df = pd.concat(dfs, ignore_index=True)
    print(f"Total rows: {len(df)}")
    
    # Feature Engineering
    df = build_features(df)
    
    print("\n--- Statistics of Engineered Features ---")
    features_to_check = ["rail_activity", "power_efficiency_ratio", "total_power", "total_movement", "avg_voltage"]
    print(df[features_to_check].describe())
    
    print("\n--- Testing Rule Engine ---")
    engine = HRSSRuleEngine()
    
    # We can evaluate rules manually to count them fast
    # Rule 1: Rail Inefficiency
    rule1 = (df["rail_activity"] > engine.rules_config["rail_activity_high"]) & \
            (df["power_efficiency_ratio"] < engine.rules_config["power_efficiency_low"])
    print(f"Rule 1 (Rail Inefficiency) triggered: {rule1.sum()} times ({(rule1.sum()/len(df))*100:.2f}%)")
    
    # Rule 2: Inefficient High Power
    rule2 = (df["total_power"] > engine.rules_config["total_power_high"]) & \
            (df["total_movement"] < engine.rules_config["total_movement_low"])
    print(f"Rule 2 (Inefficient High Power) triggered: {rule2.sum()} times ({(rule2.sum()/len(df))*100:.2f}%)")
    
    # Rule 3: Electrical Power Instability
    rule3 = df["avg_voltage"] < engine.rules_config["avg_voltage_drop"]
    print(f"Rule 3 (Electrical Power Instability) triggered: {rule3.sum()} times ({(rule3.sum()/len(df))*100:.2f}%)")

if __name__ == "__main__":
    test_data_context()
