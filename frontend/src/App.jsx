import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState('offline');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    kpi: {
      power: 0,
      efficiency: 0,
      voltage: 0
    },
    recommendation: null
  });

  // Cek koneksi ke backend saat komponen dimuat
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('http://localhost:8000/health');
        if (res.ok) setStatus('online');
        else setStatus('offline');
      } catch (e) {
        setStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  const simulateTelemetry = async () => {
    setLoading(true);
    // Dummy telemetry data (scenario: high friction, rail inefficiency)
    const payload = {
      features: {
        "O_w_BLO_power": 5.0,
        "O_w_BHL_power": 6.0,
        "O_w_BHR_power": 5.0,
        "O_w_BRU_power": 2.0,
        "O_w_HR_power": 1.0,
        "O_w_HL_power": 1.0,
        "O_w_BLO_voltage": 23.0,
        "O_w_BHL_voltage": 23.0,
        "O_w_BHR_voltage": 23.0,
        "O_w_BRU_voltage": 23.0,
        "O_w_HR_voltage": 23.0,
        "O_w_HL_voltage": 23.0,
        "I_w_BLO_Weg": 0.001,
        "I_w_BHL_Weg": 0.001,
        "I_w_BHR_Weg": 0.001,
        "I_w_BRU_Weg": 0.001,
        "I_w_HR_Weg": 0.1,
        "I_w_HL_Weg": 0.1
      }
    };

    try {
      const res = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await res.json();
      
      setData({
        kpi: {
          power: 20.0, // dummy aggregation
          efficiency: 0.005,
          voltage: 23.0
        },
        recommendation: result
      });
    } catch (e) {
      console.error("Error fetching recommendation", e);
    } finally {
      setLoading(false);
    }
  };

  const rec = data.recommendation;
  const isDanger = rec && rec.risk_level.includes("High");
  const isWarning = rec && rec.risk_level.includes("Medium");
  
  const circleClass = isDanger ? "score-circle danger" : isWarning ? "score-circle warning" : "score-circle";

  return (
    <div className="app-container">
      <header className="top-bar glass-panel">
        <h1>HRSS Operational Dashboard</h1>
        <div className="status-badge">
          <div className={`status-dot ${status}`}></div>
          {status === 'online' ? 'API Connected' : 'API Offline'}
        </div>
      </header>

      <main className="dashboard-grid">
        {/* Left Panel: Metrics & Charts */}
        <section className="left-panel">
          <div className="kpi-row">
            <div className="kpi-card glass-panel">
              <span className="kpi-title">Total Power</span>
              <span className="kpi-value highlight">{data.kpi.power.toFixed(2)} W</span>
            </div>
            <div className="kpi-card glass-panel">
              <span className="kpi-title">Avg Voltage</span>
              <span className="kpi-value">{data.kpi.voltage.toFixed(2)} V</span>
            </div>
            <div className="kpi-card glass-panel">
              <span className="kpi-title">Power Efficiency</span>
              <span className="kpi-value">{(data.kpi.efficiency * 100).toFixed(2)}%</span>
            </div>
          </div>

          <div className="chart-container glass-panel">
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem'}}>
              <h3>Live Telemetry Stream</h3>
              <button className="simulate-btn" onClick={simulateTelemetry} disabled={loading || status === 'offline'}>
                {loading ? 'Processing...' : 'Simulate Sensor Data'}
              </button>
            </div>
            <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px dashed rgba(255,255,255,0.2)', borderRadius: '8px', color: 'var(--text-secondary)'}}>
              [ Telemetry Line Chart Component Placeholder ]
            </div>
          </div>
        </section>

        {/* Right Panel: Recommendation Engine */}
        <section className="right-panel">
          <div className="recommendation-panel glass-panel">
            <h2>Recommendation Engine</h2>
            
            {rec ? (
              <>
                <div className={circleClass}>
                  <span className="score-number">{rec.efficiency_score.toFixed(0)}</span>
                  <span className="score-label">Efficiency Score</span>
                </div>

                <div style={{textAlign: 'center'}}>
                  <h3 style={{color: isDanger ? 'var(--neon-red)' : isWarning ? 'var(--neon-orange)' : 'var(--neon-green)'}}>
                    {rec.risk_level}
                  </h3>
                </div>

                {rec.rule_alerts.length > 0 && (
                  <div className="alert-box">
                    <div className="alert-title">⚠️ Domain Rules Triggered:</div>
                    <ul style={{marginLeft: '1.5rem', fontSize: '0.9rem', color: '#fca5a5'}}>
                      {rec.rule_alerts.map((alert, idx) => (
                        <li key={idx}>{alert}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div style={{marginTop: '1rem', padding: '1rem', background: 'rgba(0,0,0,0.3)', borderRadius: '8px'}}>
                  <span style={{fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase'}}>Prescriptive Action</span>
                  <p style={{marginTop: '0.5rem', fontSize: '1rem', lineHeight: '1.5'}}>{rec.actionable_recommendation}</p>
                </div>

                <button className="action-btn">
                  Acknowledge & Apply
                </button>
              </>
            ) : (
              <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)', textAlign: 'center'}}>
                Waiting for telemetry data... <br/> Click "Simulate Sensor Data" to begin.
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
