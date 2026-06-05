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

  const generateTelemetry = (scenarioType) => {
    const timestamp = Date.now() / 1000;
    const isOpt = scenarioType === 'Optimized';
    const noise = (scale) => (Math.random() - 0.5) * scale;
    
    if (isOpt) {
      return {
        Timestamp: timestamp,
        I_w_BLO_Weg: 39.05 + noise(1.0),
        I_w_BHL_Weg: 55.99 + noise(1.0),
        I_w_BHR_Weg: -8.84 + noise(0.5),
        I_w_BRU_Weg: 357.59 + noise(10.0),
        I_w_HR_Weg: -404.84 + noise(5.0),
        I_w_HL_Weg: -404.84 + noise(5.0),
        
        O_w_BLO_power: 5422.11 + noise(100.0),
        O_w_BHL_power: 4160.88 + noise(100.0),
        O_w_BHR_power: 4488.58 + noise(100.0),
        O_w_BRU_power: 6512.66 + noise(150.0),
        O_w_HR_power: 11526.51 + noise(200.0),
        O_w_HL_power: 12510.63 + noise(200.0),
        
        O_w_BLO_voltage: 14.72 + noise(0.5),
        O_w_BHL_voltage: 21.43 + noise(0.5),
        O_w_BHR_voltage: 25.30 + noise(0.5),
        O_w_BRU_voltage: 17.18 + noise(0.5),
        O_w_HR_voltage: 52.99 + noise(1.0),
        O_w_HL_voltage: 52.80 + noise(1.0),
      };
    } else {
      return {
        Timestamp: timestamp,
        I_w_BLO_Weg: 44.00 + noise(1.0),
        I_w_BHL_Weg: 56.80 + noise(1.0),
        I_w_BHR_Weg: 42.24 + noise(1.0),
        I_w_BRU_Weg: 429.01 + noise(10.0),
        I_w_HR_Weg: -411.70 + noise(5.0),
        I_w_HL_Weg: -411.70 + noise(5.0),
        
        O_w_BLO_power: 4923.84 + noise(100.0),
        O_w_BHL_power: 6996.66 + noise(100.0),
        O_w_BHR_power: 6196.42 + noise(100.0),
        O_w_BRU_power: 5116.81 + noise(150.0),
        O_w_HR_power: 11341.64 + noise(200.0),
        O_w_HL_power: 13153.05 + noise(200.0),
        
        O_w_BLO_voltage: 12.82 + noise(0.5),
        O_w_BHL_voltage: 18.50 + noise(0.5),
        O_w_BHR_voltage: 17.94 + noise(0.5),
        O_w_BRU_voltage: 13.17 + noise(0.5),
        O_w_HR_voltage: 50.29 + noise(1.0),
        O_w_HL_voltage: 50.11 + noise(1.0),
      };
    }
  };

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
      
      setStats({
        totalPower: totalP,
        avgVoltage: avgV,
        powerEfficiency: result.efficiency_score / 100
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
    const telemetry = generateTelemetry(currentScenario);
    await fetchRecommendation(telemetry);
    setLoading(false);
  };

  const startSimulation = () => {
    if (isSimulating) return;
    setIsSimulating(true);
    runSimulationStep(scenario);
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
