import React from 'react';
import { NavLink } from 'react-router-dom';
import { Activity, LayoutDashboard, LineChart, Settings, Cpu } from 'lucide-react';
import './layout.css';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Overview', icon: LayoutDashboard },
    { path: '/live', label: 'Live Monitoring', icon: Activity },
    { path: '/analytics', label: 'Analytics', icon: LineChart },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>
          <Cpu className="nav-icon" style={{ color: 'var(--color-primary)' }} />
          OptiRack HRSS
        </h1>
      </div>
      
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon className="nav-icon" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;
