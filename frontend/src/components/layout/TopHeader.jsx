import React from 'react';
import { Bell, User } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { useTelemetry } from '../../contexts/TelemetryContext';
import './layout.css';

const TopHeader = () => {
  const location = useLocation();
  const { status, isSimulating } = useTelemetry();
  
  // Simple logic to get page title from route
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': return 'System Overview';
      case '/live': return 'Live Monitoring';
      case '/analytics': return 'Historical Analytics';
      case '/settings': return 'System Settings';
      default: return 'HRSS Dashboard';
    }
  };

  return (
    <header className="top-header">
      <div className="header-title">
        {getPageTitle()}
      </div>
      
      <div className="header-actions">
        {isSimulating ? (
          <div className="status-badge" style={{ backgroundColor: 'rgba(0, 240, 255, 0.1)', color: 'var(--color-primary)', borderColor: 'rgba(0, 240, 255, 0.2)' }}>
            <div className="status-dot" style={{ backgroundColor: 'var(--color-primary)', boxShadow: '0 0 8px var(--color-primary)' }}></div>
            Live Stream Active
          </div>
        ) : (
          <div className="status-badge">
            <div className="status-dot" style={{ backgroundColor: status === 'online' ? 'var(--color-success)' : 'var(--color-danger)' }}></div>
            Model API: {status === 'online' ? 'Online' : 'Offline'}
          </div>
        )}
        
        <button className="glass-panel flex-center" style={{ width: '36px', height: '36px', background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-primary)' }}>
          <Bell size={18} />
        </button>
        
        <button className="glass-panel flex-center" style={{ width: '36px', height: '36px', background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-primary)' }}>
          <User size={18} />
        </button>
      </div>
    </header>
  );
};

export default TopHeader;
