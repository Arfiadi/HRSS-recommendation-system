import React from 'react';

export default function Header({ status }) {
  return (
    <header className="top-bar glass-panel">
      <div className="logo-section">
        <div className="pulse-indicator"></div>
        <h1>HRSS Operational Dashboard</h1>
      </div>
      <div className="status-badge">
        <div className={`status-dot ${status}`}></div>
        <span className="status-text">
          {status === 'online' ? 'API Connected' : 'API Offline'}
        </span>
      </div>
    </header>
  );
}
