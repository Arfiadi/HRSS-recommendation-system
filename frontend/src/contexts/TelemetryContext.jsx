import React, { createContext, useState, useEffect, useRef, useContext } from 'react';

const TelemetryContext = createContext(null);

export const TelemetryProvider = ({ children }) => {
  const [status, setStatus] = useState('offline');
  const [loading, setLoading] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [scenario, setScenario] = useState('Standard'); 
  const [currentMode, setCurrentMode] = useState('Standard'); 
  const [chartData, setChartData] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  
  const [stats, setStats] = useState({
    totalPower: 0,
    avgVoltage: 0,
    powerEfficiency: 0,
  });

  const simulationIntervalRef = useRef(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('http://localhost:8000/health');
        if (res.ok) {
          setStatus('online');
        } else {
          setStatus('offline');
        }
      } catch (e) {
        setStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  // Removed the unmount clearing interval, so it runs globally!
  // ONLY clear it when explicitly told to via stopSimulation.

  const stepIndexRef = useRef(0);

  useEffect(() => {
    stepIndexRef.current = 0;
    if (isSimulating) {
      runSimulationStep(scenario);
    }
  }, [scenario, isSimulating]);

  const fetchRecommendation = async (telemetry) => {
    try {
      const payload = { telemetry, current_mode: currentMode };
      const res = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("API recommendation error");
      const result = await res.json();
      setRecommendation(result);
      
      const totalP = (telemetry.O_w_BLO_power + telemetry.O_w_BHL_power + telemetry.O_w_BHR_power + telemetry.O_w_BRU_power + telemetry.O_w_HR_power + telemetry.O_w_HL_power) / 1000;
      const avgV = (telemetry.O_w_BLO_voltage + telemetry.O_w_BHL_voltage + telemetry.O_w_BHR_voltage + telemetry.O_w_BRU_voltage + telemetry.O_w_HR_voltage + telemetry.O_w_HL_voltage) / 6;
      
      setStats(prev => {
        const baselinePower = 14.5; // Average power of Standard mode
        let saved = 0;
        // Accumulate savings if the AI confirms operation is optimized and power is below baseline
        if (result.ml_predicted_profile !== 'NON-OPTIMIZED' && totalP < baselinePower) {
          // Accumulate a scaled value for demo visibility (since simulation runs fast)
          saved = (baselinePower - totalP) * 0.1;
        }

        return {
          totalPower: totalP,
          avgVoltage: avgV,
          powerEfficiency: result.efficiency_score / 100,
          totalEnergySaved: (prev.totalEnergySaved || 0) + saved
        };
      });
      
      setChartData(prev => {
        const timeStr = new Date(telemetry.Timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const nextData = [...prev, {
          time: timeStr,
          power: parseFloat(totalP.toFixed(2)),
          voltage: parseFloat(avgV.toFixed(2)),
          efficiency: result.efficiency_score,
        }];
        if (nextData.length > 15) return nextData.slice(nextData.length - 15);
        return nextData;
      });
    } catch (e) {
      console.error("Failed to fetch recommendation:", e);
    }
  };

  const runSimulationStep = async (currentScenario) => {
    setLoading(true);
    try {
      const idx = stepIndexRef.current;
      const res = await fetch(`http://localhost:8000/api/v1/simulate/telemetry?scenario=${currentScenario}&index=${idx}`);
      if (!res.ok) throw new Error("Failed to fetch simulated telemetry");
      const telemetry = await res.json();
      await fetchRecommendation(telemetry);
      stepIndexRef.current += 1;
    } catch (e) {
      console.error("Failed to run simulation step:", e);
    } finally {
      setLoading(false);
    }
  };

  const startSimulation = () => {
    if (isSimulating) return;
    setIsSimulating(true);
    simulationIntervalRef.current = setInterval(() => {
      setScenario(prevScenario => {
        runSimulationStep(prevScenario);
        return prevScenario;
      });
    }, 2000);
  };

  const stopSimulation = () => {
    if (!isSimulating) return;
    setIsSimulating(false);
    if (simulationIntervalRef.current) {
      clearInterval(simulationIntervalRef.current);
      simulationIntervalRef.current = null;
    }
  };

  const toggleSimulation = () => {
    if (isSimulating) {
      stopSimulation();
    } else {
      startSimulation();
    }
  };

  const value = {
    status, loading, isSimulating, scenario, setScenario,
    currentMode, setCurrentMode, chartData, recommendation,
    stats, toggleSimulation, runSimulationStep
  };

  return (
    <TelemetryContext.Provider value={value}>
      {children}
    </TelemetryContext.Provider>
  );
};

export const useTelemetry = () => useContext(TelemetryContext);
