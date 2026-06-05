import React from 'react';
import { BarChart, AreaChart } from 'lucide-react';

const Analytics = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-xl)' }}>
      <div>
        <h1>Historical Analytics</h1>
        <p>Review past telemetry data, machine learning performance, and efficiency trends.</p>
      </div>

      <div className="glass-panel flex-center" style={{ height: '400px', flexDirection: 'column', gap: 'var(--gap-md)' }}>
        <AreaChart size={48} color="var(--text-muted)" />
        <h3 style={{ color: 'var(--text-muted)' }}>Historical Data Visualization Coming Soon</h3>
        <p style={{ maxWidth: '400px', textAlign: 'center' }}>
          This module will be connected to the historical telemetry database to show long-term efficiency and anomaly distributions.
        </p>
      </div>
    </div>
  );
};

export default Analytics;
