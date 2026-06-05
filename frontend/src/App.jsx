import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Overview from './pages/Overview';
import LiveMonitoring from './pages/LiveMonitoring';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import { TelemetryProvider } from './contexts/TelemetryContext';

function App() {
  return (
    <TelemetryProvider>
      <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Overview />} />
          <Route path="live" element={<LiveMonitoring />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </Router>
    </TelemetryProvider>
  );
}

export default App;
