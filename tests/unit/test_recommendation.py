"""
Unit Test — Recommendation Module.
"""
import pandas as pd
from src.recommendation.rule_engine import HRSSRuleEngine
from src.recommendation.decision_policy import generate_decision
from src.recommendation.scoring import calculate_efficiency_score


def test_rule_engine_normal():
    engine = HRSSRuleEngine()
    # Data normal
    df = pd.DataFrame(
        [
            {
                "rail_activity": 0.01,
                "power_efficiency_ratio": 0.05,
                "total_power": 5.0,
                "total_movement": 0.1,
                "avg_voltage": 24.0,
            }
        ]
    )
    alerts = engine.evaluate_rules(df)
    assert len(alerts) == 0


def test_rule_engine_anomalies():
    engine = HRSSRuleEngine()

    # Test Rule 1: Rail Inefficiency
    df_rail = pd.DataFrame(
        [
            {
                "rail_activity": 0.1,  # > 0.05
                "power_efficiency_ratio": 0.005,  # < 0.01
            }
        ]
    )
    alerts_rail = engine.evaluate_rules(df_rail)
    assert any("Rail Inefficiency" in alert for alert in alerts_rail)

    # Test Rule 2: Inefficient High Power (Movement Inefficiency)
    df_friction = pd.DataFrame(
        [
            {
                "total_power": 20.0,  # > 15.0
                "total_movement": 0.005,  # < 0.02
            }
        ]
    )
    alerts_friction = engine.evaluate_rules(df_friction)
    assert any("Movement Inefficiency" in alert for alert in alerts_friction)

    # Test Rule 3: Power Instability (Voltage Sag)
    df_voltage = pd.DataFrame(
        [
            {
                "avg_voltage": 22.0,  # < 23.5
            }
        ]
    )
    alerts_voltage = engine.evaluate_rules(df_voltage)
    assert any("Power Instability" in alert for alert in alerts_voltage)


def test_decision_policy():
    # Skenario 1: Normal
    risk, action = generate_decision("Standard", "Standard", 0.1, [])
    assert risk == "Optimal Efficiency"

    # Skenario 2: Medium Inefficiency (ML beda, no alerts)
    risk, action = generate_decision("Standard", "Optimized", 0.9, [])
    assert risk == "Sub-optimal Movement"

    # Skenario 3: High Inefficiency (Alerts terpicu)
    risk, action = generate_decision(
        "Optimized", "Standard", 0.1, ["Power Instability alert"]
    )
    assert risk == "Critical Inefficiency"


def test_scoring():
    df = pd.DataFrame([{}])
    # Case 1: Optimized prob 80%, no alerts
    score = calculate_efficiency_score(df, 0.8, [])
    assert score == 80.0

    # Case 2: Penalti dari Rail Inefficiency (80% - 30% = 50%)
    score = calculate_efficiency_score(df, 0.8, ["Rail Inefficiency alert"])
    assert score == 50.0

    # Case 3: Batas bawah 0%
    score = calculate_efficiency_score(
        df, 0.2, ["Rail Inefficiency alert", "Movement Inefficiency alert"]
    )
    assert score == 0.0
