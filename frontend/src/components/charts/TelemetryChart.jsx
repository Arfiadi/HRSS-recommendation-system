import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

export default function TelemetryChart({ data, isSimulating, onToggle, status, loading }) {
  return (
    <div className="chart-container glass-panel">
      <div className="chart-header">
        <div className="chart-title-section">
          <h3>Live Telemetry Stream</h3>
          <p className="chart-subtitle">Real-time Power & Voltage monitoring</p>
        </div>
        
        <button 
          className={`simulate-btn ${isSimulating ? 'simulating' : ''}`} 
          onClick={onToggle} 
          disabled={status === 'offline' || loading}
        >
          <span className="btn-icon"></span>
          {isSimulating ? 'Stop Stream' : 'Start Live Stream'}
        </button>
      </div>
      
      <div className="chart-wrapper">
        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorPower" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorVoltage" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
              <XAxis 
                dataKey="time" 
                stroke="#64748b" 
                fontSize={10} 
                tickLine={false} 
              />
              <YAxis 
                yAxisId="left"
                stroke="#3b82f6" 
                fontSize={10}
                tickLine={false}
                axisLine={false}
                label={{ value: 'Power (W)', angle: -90, position: 'insideLeft', style: { fill: '#3b82f6', fontSize: 10 } }}
              />
              <YAxis 
                yAxisId="right"
                orientation="right"
                stroke="#8b5cf6" 
                fontSize={10}
                tickLine={false}
                axisLine={false}
                label={{ value: 'Voltage (V)', angle: 90, position: 'insideRight', style: { fill: '#8b5cf6', fontSize: 10 } }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.5)',
                  color: '#f8fafc'
                }}
              />
              <Legend verticalAlign="top" height={36} iconType="circle" />
              <Area 
                yAxisId="left"
                type="monotone" 
                dataKey="power" 
                name="Total Power (W)" 
                stroke="#3b82f6" 
                strokeWidth={2}
                fillOpacity={1} 
                fill="url(#colorPower)" 
                activeDot={{ r: 6, strokeWidth: 0 }}
              />
              <Area 
                yAxisId="right"
                type="monotone" 
                dataKey="voltage" 
                name="Avg Voltage (V)" 
                stroke="#8b5cf6" 
                strokeWidth={2}
                fillOpacity={1} 
                fill="url(#colorVoltage)" 
                activeDot={{ r: 6, strokeWidth: 0 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="chart-placeholder">
            <div className="pulse-loader"></div>
            <span>Waiting for simulation data... Click Start Live Stream.</span>
          </div>
        )}
      </div>
    </div>
  );
}
