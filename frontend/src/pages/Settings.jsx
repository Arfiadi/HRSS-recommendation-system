import React from 'react';
import { Settings as SettingsIcon } from 'lucide-react';

const Settings = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-xl)' }}>
      <div>
        <h1>System Settings</h1>
        <p>Configure model thresholds, notification rules, and API connections.</p>
      </div>

      <div className="glass-panel" style={{ padding: 'var(--gap-xl)', maxWidth: '600px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--gap-md)', marginBottom: 'var(--gap-lg)' }}>
          <SettingsIcon color="var(--color-primary)" />
          <h3>Model Configuration</h3>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--gap-md)' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: 'var(--font-sm)', color: 'var(--text-secondary)' }}>Active ML Model</label>
            <select className="glass-panel" style={{ padding: '10px', color: 'var(--text-primary)', border: '1px solid var(--glass-border-focus)', outline: 'none' }}>
              <option value="rf">Random Forest Classifier (Champion)</option>
              <option value="gb">Gradient Boosting (Challenger)</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: 'var(--font-sm)', color: 'var(--text-secondary)' }}>Warning Threshold (Efficiency)</label>
            <input type="range" min="0" max="100" defaultValue="70" style={{ accentColor: 'var(--color-primary)' }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
