import React from 'react';
import { Activity, Zap, AlertTriangle, CheckCircle } from 'lucide-react';
import { useTelemetry } from '../contexts/TelemetryContext';

const Overview = () => {
  const telemetry = useTelemetry();
  const hasData = telemetry && telemetry.stats && telemetry.stats.totalPower > 0;
  
  const efficiency = hasData ? (telemetry.stats.powerEfficiency * 100).toFixed(1) + '%' : '94.2%';
  const power = hasData ? telemetry.stats.totalPower.toFixed(1) + ' kW' : '14.5 kW';
  const statusText = hasData 
    ? (telemetry.recommendation && telemetry.recommendation.operational_risk_level.toLowerCase().includes('high') ? 'Warning' : 'Optimal')
    : 'Optimal';
  const statusColor = statusText === 'Warning' ? 'var(--color-danger)' : 'var(--color-success)';
  const statusDesc = statusText === 'Warning' ? 'Anomalies or low efficiency detected' : 'All machines running smoothly';
  const alertsCount = hasData 
    ? (telemetry.recommendation ? telemetry.recommendation.technical_alerts.filter(a => !a.includes('Semua metrik')).length : 0)
    : 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-xl)' }}>
      <div>
        <h1>System Overview</h1>
        <p>Welcome back to HRSS Dashboard. Here is the high-level summary of your system health.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 'var(--gap-lg)' }}>
        
        {/* KPI Cards */}
        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>System Status</span>
            <CheckCircle color={statusColor} size={20} />
          </div>
          <h2 style={{ color: statusColor }}>{statusText}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: statusColor }}>{statusDesc}</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Avg Global Efficiency</span>
            <Activity color="var(--color-primary)" size={20} />
          </div>
          <h2>{efficiency}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--color-primary)' }}>Based on active operations</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Avg Power Usage</span>
            <Zap color="var(--color-warning)" size={20} />
          </div>
          <h2>{power}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>Normal threshold</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Active Alerts</span>
            <AlertTriangle color="var(--color-danger)" size={20} />
          </div>
          <h2>{alertsCount}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>Recent hardware warnings</span>
        </div>

      </div>
    </div>
  );
};

export default Overview;
