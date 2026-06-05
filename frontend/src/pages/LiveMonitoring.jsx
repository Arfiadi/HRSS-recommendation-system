import React from 'react';
import { useTelemetry } from '../contexts/TelemetryContext';
import KpiCard from '../components/cards/KpiCard';
import TelemetryChart from '../components/charts/TelemetryChart';
import RecommendationPanel from '../components/panels/RecommendationPanel';
import '../App.css'; // Still keeping old css for components specific styles

const LiveMonitoring = () => {
  const {
    status,
    loading,
    isSimulating,
    scenario,
    setScenario,
    currentMode,
    setCurrentMode,
    chartData,
    recommendation,
    stats,
    toggleSimulation
  } = useTelemetry();

  // Determine if total power is exceeding critical thresholds to highlight the card
  const isPowerExceeded = stats.totalPower > 15; // > 15W is high for this machinery configuration

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-lg)' }}>
      {/* KPI Cards Row */}
      <section className="kpi-row">
        <KpiCard 
          title="Aggregated Power" 
          value={stats.totalPower.toFixed(2)} 
          unit="W" 
          type="power"
          isWarning={isPowerExceeded}
        />
        <KpiCard 
          title="Avg Operating Voltage" 
          value={stats.avgVoltage.toFixed(2)} 
          unit="V" 
          type="voltage"
        />
        <KpiCard 
          title="System Energy Efficiency" 
          value={(stats.powerEfficiency * 100).toFixed(1)} 
          unit="%" 
          type="efficiency"
        />
      </section>

      {/* Dashboard Panels Grid */}
      <div className="dashboard-grid">
        <section className="left-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <TelemetryChart 
            data={chartData} 
            isSimulating={isSimulating}
            onToggle={toggleSimulation}
            status={status}
            loading={loading}
          />
          
          <div className="glass-panel" style={{ padding: '1.5rem 1.75rem' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 600, borderBottom: '1px solid rgba(255, 255, 255, 0.06)', paddingBottom: '0.75rem', marginBottom: '1rem' }}>Simulation & Machine State</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <div className="control-group" style={{ marginBottom: 0 }}>
                <label>Machinery Scenario:</label>
                <div className="toggle-buttons">
                  <button 
                    className={`toggle-btn std ${scenario === 'Standard' ? 'active' : ''}`}
                    onClick={() => setScenario('Standard')}
                  >
                    Standard Rail
                  </button>
                  <button 
                    className={`toggle-btn opt ${scenario === 'Optimized' ? 'active' : ''}`}
                    onClick={() => setScenario('Optimized')}
                  >
                    Simultaneous
                  </button>
                </div>
              </div>

              <div className="control-group" style={{ marginBottom: 0 }}>
                <label>Actual Machine State:</label>
                <select 
                  value={currentMode} 
                  onChange={(e) => setCurrentMode(e.target.value)}
                  className="mode-select"
                  style={{ padding: '0.6rem' }}
                >
                  <option value="Standard">Standard Pattern</option>
                  <option value="Optimized">Optimized Pattern</option>
                </select>
              </div>
            </div>
          </div>
        </section>

        <section className="right-panel">
          <RecommendationPanel 
            recommendation={recommendation}
            scenario={scenario}
            setScenario={setScenario}
            currentMode={currentMode}
            setCurrentMode={setCurrentMode}
            isSimulating={isSimulating}
          />
        </section>
      </div>
    </div>
  );
};

export default LiveMonitoring;
