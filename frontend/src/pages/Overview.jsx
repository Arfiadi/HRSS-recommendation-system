import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, Zap, AlertTriangle, CheckCircle, BarChart2, Activity as ActivityIcon, Server, Cpu, PlayCircle, Settings } from 'lucide-react';
import { useTelemetry } from '../contexts/TelemetryContext';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

const Overview = () => {
  const telemetry = useTelemetry();
  const navigate = useNavigate();
  const hasData = telemetry && telemetry.stats && telemetry.stats.totalPower > 0;
  
  const efficiency = hasData ? (telemetry.stats.powerEfficiency * 100).toFixed(1) + '%' : '94.2%';
  const power = hasData ? telemetry.stats.totalPower.toFixed(1) + ' W' : '14.5 W';
  
  // Predict if the system is running in NON-OPTIMIZED mode
  const isNonOptimized = hasData && telemetry.recommendation && telemetry.recommendation.ml_predicted_profile === 'NON-OPTIMIZED';
  
  const statusText = isNonOptimized ? 'Sub-optimal' : 'Optimal';
  const statusColor = isNonOptimized ? 'var(--color-warning)' : 'var(--color-success)';
  const statusDesc = isNonOptimized ? 'Inefficient movement pattern detected' : 'Simultaneous movement active';
  
  const inefficientCount = hasData && isNonOptimized ? 1 : 0;

  // Mock data for ROI Savings chart (Comparing Standard vs Optimized mode energy usage)
  const savingsData = [
    { name: 'Mon', Standard: 120, Optimized: 90 },
    { name: 'Tue', Standard: 130, Optimized: 95 },
    { name: 'Wed', Standard: 125, Optimized: 88 },
    { name: 'Thu', Standard: 140, Optimized: 100 },
    { name: 'Fri', Standard: 135, Optimized: 92 },
    { name: 'Sat', Standard: 110, Optimized: 80 },
    { name: 'Sun', Standard: 105, Optimized: 75 },
  ];

  // Dynamic Event Log simulation based on telemetry changes
  const [eventLog, setEventLog] = useState([
    { id: 1, time: '08:00 AM', type: 'info', message: 'HRSS telemetry stream initialized.' },
    { id: 2, time: '08:15 AM', type: 'success', message: 'Optimization Engine engaged.' }
  ]);

  useEffect(() => {
    if (hasData && telemetry.recommendation) {
      const isNowNonOptimized = telemetry.recommendation.ml_predicted_profile === 'NON-OPTIMIZED';
      const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      
      setEventLog(prev => {
        const lastEvent = prev[0];
        // Only log if the state changed
        if (isNowNonOptimized && (!lastEvent || !lastEvent.message.includes('Standard Operation'))) {
          return [{ id: Date.now(), time: timestamp, type: 'warning', message: 'Standard Operation detected. Recommendation: Apply simultaneous movement.' }, ...prev].slice(0, 5);
        } else if (!isNowNonOptimized && (!lastEvent || !lastEvent.message.includes('Simultaneous'))) {
          return [{ id: Date.now(), time: timestamp, type: 'success', message: 'Simultaneous Movement (Optimized) confirmed. Energy consumption lowering.' }, ...prev].slice(0, 5);
        }
        return prev;
      });
    }
  }, [telemetry.recommendation, hasData]);

  // Nodes for the Status Grid
  const nodes = [
    { name: 'Middle Conveyor Belt', status: 'Active', type: 'hardware' },
    { name: 'Rail System', status: 'Active', type: 'hardware' },
    { name: 'Movement Controller', status: isNonOptimized ? 'Standard Mode' : 'Optimized Mode', type: 'hardware' },
    { name: 'Optimization Engine', status: 'Online', type: 'software' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-xl)' }}>
      <div>
        <h1>OptiRack HRSS Operational Efficiency</h1>
        <p>High-level summary of High Rack Storage System movement efficiency and energy consumption.</p>
      </div>

      {/* KPI Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--gap-lg)' }}>
        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Operational Status</span>
            <CheckCircle color={statusColor} size={20} />
          </div>
          <h2 style={{ color: statusColor }}>{statusText}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: statusColor }}>{statusDesc}</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Movement Efficiency</span>
            <Activity color="var(--color-primary)" size={20} />
          </div>
          <h2>{efficiency}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--color-primary)' }}>Based on current operation</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Power Consumption</span>
            <Zap color="var(--color-warning)" size={20} />
          </div>
          <h2>{power}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>Telemetry sensor average</span>
        </div>

        <div className="glass-panel" style={{ padding: 'var(--gap-lg)', display: 'flex', flexDirection: 'column', gap: 'var(--gap-sm)' }}>
          <div className="flex-between">
            <span style={{ color: 'var(--text-secondary)' }}>Inefficient Cycles</span>
            <AlertTriangle color="var(--color-warning)" size={20} />
          </div>
          <h2>{inefficientCount}</h2>
          <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>Non-simultaneous movements</span>
        </div>
      </div>

      {/* Main Content Grid: Top Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 'var(--gap-lg)' }}>
        
        {/* 1. AI Impact & Savings Panel */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
          <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BarChart2 size={18} color="var(--color-success)" /> Operation Strategy Impact</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Estimated power consumption: Standard vs Optimized Mode (kWh)</p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Live Energy Saved</span>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--color-success)' }}>
                {telemetry && telemetry.stats && telemetry.stats.totalEnergySaved 
                  ? telemetry.stats.totalEnergySaved.toFixed(2) 
                  : '0.00'} kWh
              </div>
            </div>
          </div>
          
          <div style={{ flex: 1, minHeight: '220px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={savingsData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-secondary)" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--text-secondary)" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  contentStyle={{ backgroundColor: 'rgba(11, 15, 25, 0.95)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="Standard" fill="#64748B" radius={[4, 4, 0, 0]} name="Standard Operation (Non-Simultaneous)" />
                <Bar dataKey="Optimized" fill="var(--color-primary)" radius={[4, 4, 0, 0]} name="Optimized Operation (Simultaneous)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 2. Recent Activity & Event Log */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}><ActivityIcon size={18} color="var(--color-warning)" /> Movement Strategy Log</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1, overflowY: 'auto' }}>
            {eventLog.map(log => (
              <div key={log.id} style={{ display: 'flex', gap: '0.75rem', borderLeft: `2px solid ${log.type === 'warning' ? 'var(--color-warning)' : log.type === 'success' ? 'var(--color-success)' : 'var(--color-primary)'}`, paddingLeft: '0.75rem' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', minWidth: '60px' }}>{log.time}</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>{log.message}</div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Main Content Grid: Bottom Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--gap-lg)' }}>
        
        {/* 3. Sub-System / Node Status Grid */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}><Server size={18} color="var(--color-secondary)" /> HRSS Components Status</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            {nodes.map((node, i) => (
              <div key={i} style={{ padding: '0.75rem', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ padding: '0.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '6px' }}>
                  {node.type === 'software' ? <Server size={16} color="var(--color-secondary)"/> : <Cpu size={16} color="var(--text-secondary)" />}
                </div>
                <div>
                  <div style={{ fontSize: '0.8rem', fontWeight: 600 }}>{node.name}</div>
                  <div style={{ fontSize: '0.7rem', color: node.status === 'Optimized Mode' || node.status === 'Active' || node.status === 'Online' ? 'var(--color-success)' : 'var(--color-warning)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: node.status === 'Optimized Mode' || node.status === 'Active' || node.status === 'Online' ? 'var(--color-success)' : 'var(--color-warning)' }}></span>
                    {node.status}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 4. Quick Action Shortcuts */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ marginBottom: '1rem' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <button 
              className="action-btn" 
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: 'linear-gradient(135deg, #8A2BE2, #4c1d95)' }}
              onClick={() => navigate('/live')}
            >
              <PlayCircle size={18} /> Enter Live Telemetry
            </button>
            <button 
              className="action-btn" 
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: 'white', boxShadow: 'none' }}
              onClick={() => alert("Simulation strategy recalibrated. The Optimization Engine is ready.")}
            >
              <Settings size={18} /> Recalibrate AI Strategy
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Overview;
