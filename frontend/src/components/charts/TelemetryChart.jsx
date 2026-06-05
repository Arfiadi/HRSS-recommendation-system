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
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorPower" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00F0FF" stopOpacity={0.6}/>
                  <stop offset="95%" stopColor="#00F0FF" stopOpacity={0.05}/>
                </linearGradient>
                <linearGradient id="colorVoltage" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8A2BE2" stopOpacity={0.6}/>
                  <stop offset="95%" stopColor="#8A2BE2" stopOpacity={0.05}/>
                </linearGradient>
                <filter id="glowPower" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <filter id="glowVoltage" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" vertical={false} />
              <XAxis 
                dataKey="time" 
                stroke="#94A3B8" 
                fontSize={11} 
                tickLine={false} 
                axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
              />
              <YAxis 
                yAxisId="left"
                stroke="#00F0FF" 
                fontSize={11}
                tickLine={false}
                axisLine={false}
                label={{ value: 'Power (W)', angle: -90, position: 'insideLeft', style: { fill: '#00F0FF', fontSize: 11, fontWeight: 500 } }}
              />
              <YAxis 
                yAxisId="right"
                orientation="right"
                stroke="#8A2BE2" 
                fontSize={11}
                tickLine={false}
                axisLine={false}
                label={{ value: 'Voltage (V)', angle: 90, position: 'insideRight', style: { fill: '#8A2BE2', fontSize: 11, fontWeight: 500 } }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(11, 15, 25, 0.95)', 
                  border: '1px solid rgba(0, 240, 255, 0.3)',
                  borderRadius: '8px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
                  color: '#E2E8F0',
                  backdropFilter: 'blur(8px)'
                }}
                itemStyle={{ color: '#E2E8F0', fontWeight: 500 }}
              />
              <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px', fontWeight: 500 }} />
              <Area 
                yAxisId="left"
                type="monotone" 
                dataKey="power" 
                name="Total Power (W)" 
                stroke="#00F0FF" 
                strokeWidth={3}
                fillOpacity={1} 
                fill="url(#colorPower)" 
                activeDot={{ r: 6, fill: '#00F0FF', stroke: '#fff', strokeWidth: 2, filter: 'url(#glowPower)' }}
                filter="url(#glowPower)"
              />
              <Area 
                yAxisId="right"
                type="monotone" 
                dataKey="voltage" 
                name="Avg Voltage (V)" 
                stroke="#8A2BE2" 
                strokeWidth={3}
                fillOpacity={1} 
                fill="url(#colorVoltage)" 
                activeDot={{ r: 6, fill: '#8A2BE2', stroke: '#fff', strokeWidth: 2, filter: 'url(#glowVoltage)' }}
                filter="url(#glowVoltage)"
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
