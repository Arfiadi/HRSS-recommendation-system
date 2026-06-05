import React, { useState } from 'react';

export default function RecommendationPanel({
  recommendation,
  scenario,
  setScenario,
  currentMode,
  setCurrentMode,
  isSimulating
}) {
  const [acknowledged, setAcknowledged] = useState(false);

  const handleAcknowledge = () => {
    setAcknowledged(true);
    setTimeout(() => setAcknowledged(false), 3000);
  };

  const isOpt = scenario === 'Optimized';
  
  // Scoring styling helpers
  const score = recommendation ? recommendation.efficiency_score : 0;
  const isHighRisk = recommendation && recommendation.operational_risk_level.toLowerCase().includes('high');
  const isMediumRisk = recommendation && recommendation.operational_risk_level.toLowerCase().includes('medium');
  
  let scoreColorClass = 'score-circle-svg-green';
  let riskColorClass = 'risk-low';
  if (isHighRisk) {
    scoreColorClass = 'score-circle-svg-red';
    riskColorClass = 'risk-high';
  } else if (isMediumRisk) {
    scoreColorClass = 'score-circle-svg-orange';
    riskColorClass = 'risk-medium';
  }

  // Circular progress stroke dash calculation
  // Radius = 50, Circumference = 2 * PI * r = ~314
  const strokeDashoffset = 314 - (314 * score) / 100;

  return (
    <div className="recommendation-panel glass-panel">
      <h2>Recommendation Engine</h2>
      
      {recommendation ? (
        <div className="rec-details-container fade-in">
          {/* Circular Score representation */}
          <div className="score-container">
            <div className="svg-circular-progress">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" className="circle-bg" />
                <circle 
                  cx="60" 
                  cy="60" 
                  r="50" 
                  className={`circle-progress ${scoreColorClass}`}
                  strokeDasharray="314"
                  strokeDashoffset={strokeDashoffset}
                />
              </svg>
              <div className="score-text-overlay">
                <span className="overlay-number">{score.toFixed(0)}</span>
                <span className="overlay-label">Efficiency</span>
              </div>
            </div>
          </div>

          <div className="rec-badges-row">
            <div className="badge-item">
              <span className="badge-label">AI Profile</span>
              <span className="badge-value highlight-blue">{recommendation.ml_predicted_profile}</span>
            </div>
            <div className="badge-item">
              <span className="badge-label">Operational Risk</span>
              <span className={`badge-value ${riskColorClass}`}>{recommendation.operational_risk_level}</span>
            </div>
          </div>

          {recommendation.technical_alerts.length > 0 && (
            <div className="alert-box">
              <div className="alert-header">
                <span className="alert-icon">⚠️</span>
                <span>Rule Violations / Alerts ({recommendation.technical_alerts.length})</span>
              </div>
              <ul className="alert-list">
                {recommendation.technical_alerts.map((alert, idx) => (
                  <li key={idx} className="alert-item">{alert}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="prescriptive-card">
            <span className="prescriptive-title">Prescriptive Recommendation</span>
            <p className="prescriptive-text">{recommendation.primary_recommendation}</p>
          </div>

          <button 
            className={`action-btn ${acknowledged ? 'acknowledged' : ''}`}
            onClick={handleAcknowledge}
            disabled={acknowledged}
          >
            {acknowledged ? '✓ Actions Dispatched' : 'Acknowledge & Adjust Pattern'}
          </button>
        </div>
      ) : (
        <div className="rec-empty-state">
          <div className="scanner-line"></div>
          <p>
            {isSimulating 
              ? 'Fetching telemetry predictions...' 
              : 'Dashboard Standby. Start Live Stream to feed sensor data into the Recommendation Engine.'}
          </p>
        </div>
      )}
    </div>
  );
}
