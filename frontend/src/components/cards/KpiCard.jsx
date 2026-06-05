import React from 'react';

export default function KpiCard({ title, value, unit, type = 'default', isWarning = false }) {
  const cardClass = `kpi-card glass-panel ${type} ${isWarning ? 'alert-pulse' : ''}`;
  
  return (
    <div className={cardClass}>
      <span className="kpi-title">{title}</span>
      <div className="kpi-value-container">
        <span className="kpi-value">{value}</span>
        <span className="kpi-unit">{unit}</span>
      </div>
      <div className="card-ambient-glow"></div>
    </div>
  );
}
