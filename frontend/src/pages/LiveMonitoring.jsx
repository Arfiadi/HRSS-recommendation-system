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
        <section className="left-panel">
          <TelemetryChart 
            data={chartData} 
            isSimulating={isSimulating}
            onToggle={toggleSimulation}
            status={status}
            loading={loading}
          />
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
