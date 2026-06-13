import { useState, useEffect, useRef } from 'react';

export function useTelemetry() {
  const [status, setStatus] = useState('offline');
  const [loading, setLoading] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [scenario, setScenario] = useState('Standard'); // 'Standard' or 'Optimized'
  const [currentMode, setCurrentMode] = useState('Standard'); // Machine mode sent to API
  const [chartData, setChartData] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  
  // Track aggregated stats
  const [stats, setStats] = useState({
    totalPower: 0,
    avgVoltage: 0,
    powerEfficiency: 0,
  });

  const simulationIntervalRef = useRef(null);

  // Check backend health
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

  // Stop simulation on unmount
  useEffect(() => {
    return () => {
      if (simulationIntervalRef.current) {
        clearInterval(simulationIntervalRef.current);
      }
    };
  }, []);

  // Function to generate simulated telemetry data based on scenario
  const generateTelemetry = (scenarioType) => {
    const timestamp = Date.now() / 1000;
    
    // In Standard scenario: high power usage, low movement coordination, etc.
    // In Optimized scenario: balanced/low power usage, coordinated movements.
    const isOpt = scenarioType === 'Optimized';
    
    const noise = () => (Math.random() - 0.5) * 0.05;
    
    // Adjust values to trigger/not trigger specific rules in rule_engine.py
    return {
      Timestamp: timestamp,
      // Weg (displacement) - ranges around 0.1 to 1.5
      // If optimized: high coordinated movements (1.2m)
      // If standard: small movements (0.08m horizontal rail) to trigger rail inefficiency
      I_w_BLO_Weg: isOpt ? 1.2 + noise() : 0.02 + noise(),
      I_w_BHL_Weg: isOpt ? 1.1 + noise() : 0.02 + noise(),
      I_w_BHR_Weg: isOpt ? 1.1 + noise() : 0.02 + noise(),
      I_w_BRU_Weg: isOpt ? 0.8 + noise() : 0.01 + noise(),
      I_w_HR_Weg: isOpt ? 1.4 + noise() : 0.08 + noise(),
      I_w_HL_Weg: isOpt ? 1.4 + noise() : 0.08 + noise(),
      
      // Power (Watts) - much higher in standard mode (triggers > 15W check)
      O_w_BLO_power: isOpt ? 0.8 + noise() : 2.5 + noise(),
      O_w_BHL_power: isOpt ? 1.0 + noise() : 3.8 + noise(),
      O_w_BHR_power: isOpt ? 1.0 + noise() : 3.8 + noise(),
      O_w_BRU_power: isOpt ? 0.6 + noise() : 2.2 + noise(),
      O_w_HR_power: isOpt ? 0.9 + noise() : 4.5 + noise(),
      O_w_HL_power: isOpt ? 0.9 + noise() : 4.5 + noise(),
      
      // Voltage (Volts) - drops under 23.5V in standard (triggers Voltage Sag)
      O_w_BLO_voltage: isOpt ? 24.1 + noise() : 23.2 + noise(),
      O_w_BHL_voltage: isOpt ? 24.0 + noise() : 23.1 + noise(),
      O_w_BHR_voltage: isOpt ? 24.0 + noise() : 23.1 + noise(),
      O_w_BRU_voltage: isOpt ? 24.1 + noise() : 23.3 + noise(),
      O_w_HR_voltage: isOpt ? 24.0 + noise() : 23.2 + noise(),
      O_w_HL_voltage: isOpt ? 24.0 + noise() : 23.2 + noise(),
    };
  };

  const fetchRecommendation = async (telemetry) => {
    try {
      const payload = {
        telemetry,
        current_mode: currentMode
      };
      
      const res = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) throw new Error("API recommendation error");
      
      const result = await res.json();
      setRecommendation(result);
      
      // Calculate display metrics from telemetry and recommendation
      const totalP = 
        telemetry.O_w_BLO_power + 
        telemetry.O_w_BHL_power + 
        telemetry.O_w_BHR_power + 
        telemetry.O_w_BRU_power + 
        telemetry.O_w_HR_power + 
        telemetry.O_w_HL_power;
        
      const avgV = (
        telemetry.O_w_BLO_voltage + 
        telemetry.O_w_BHL_voltage + 
        telemetry.O_w_BHR_voltage + 
        telemetry.O_w_BRU_voltage + 
        telemetry.O_w_HR_voltage + 
        telemetry.O_w_HL_voltage
      ) / 6;
      
      setStats({
        totalPower: totalP,
        avgVoltage: avgV,
        powerEfficiency: result.efficiency_score / 100
      });
      
      // Update chart history (keep last 15 points)
      setChartData(prev => {
        const timeStr = new Date(telemetry.Timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const nextData = [...prev, {
          time: timeStr,
          power: parseFloat(totalP.toFixed(2)),
          voltage: parseFloat(avgV.toFixed(2)),
          efficiency: result.efficiency_score,
        }];
        if (nextData.length > 15) {
          return nextData.slice(nextData.length - 15);
        }
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
    
    // Run initial immediately
    runSimulationStep(scenario);
    
    simulationIntervalRef.current = setInterval(() => {
      // Use state updater to get freshest scenario
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

  return {
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
    toggleSimulation,
    runSimulationStep
  };
}
