import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RecommendationPanel from './RecommendationPanel';

describe('RecommendationPanel Component', () => {
  const mockRecommendation = {
    efficiency_score: 85,
    ml_predicted_profile: 'Optimized',
    operational_risk_level: 'Low Risk',
    technical_alerts: ['Friction normal', 'Voltage normal'],
    primary_recommendation: 'Maintain current pattern.'
  };

  test('renders standby empty state when recommendation is null and isSimulating is false', () => {
    render(
      <RecommendationPanel 
        recommendation={null}
        scenario="Standard"
        setScenario={vi.fn()}
        currentMode="Standard"
        setCurrentMode={vi.fn()}
        isSimulating={false}
      />
    );
    expect(screen.getByText(/Dashboard Standby/i)).toBeInTheDocument();
  });

  test('renders fetching state when recommendation is null and isSimulating is true', () => {
    render(
      <RecommendationPanel 
        recommendation={null}
        scenario="Standard"
        setScenario={vi.fn()}
        currentMode="Standard"
        setCurrentMode={vi.fn()}
        isSimulating={true}
      />
    );
    expect(screen.getByText(/Fetching telemetry predictions/i)).toBeInTheDocument();
  });

  test('renders recommendation details when provided', () => {
    render(
      <RecommendationPanel 
        recommendation={mockRecommendation}
        scenario="Standard"
        setScenario={vi.fn()}
        currentMode="Standard"
        setCurrentMode={vi.fn()}
        isSimulating={true}
      />
    );

    expect(screen.getByText('85')).toBeInTheDocument();
    expect(screen.getByText('AI Profile')).toBeInTheDocument();
    expect(screen.getByText('Optimized')).toBeInTheDocument();
    expect(screen.getByText('Operational Risk')).toBeInTheDocument();
    expect(screen.getByText('Low Risk')).toBeInTheDocument();
    expect(screen.getByText('Maintain current pattern.')).toBeInTheDocument();
    expect(screen.getByText('Rule Violations / Alerts (2)')).toBeInTheDocument();
  });

  test('calls setScenario when scenario buttons are clicked', () => {
    const setScenarioMock = vi.fn();
    render(
      <RecommendationPanel 
        recommendation={mockRecommendation}
        scenario="Standard"
        setScenario={setScenarioMock}
        currentMode="Standard"
        setCurrentMode={vi.fn()}
        isSimulating={true}
      />
    );

    const optimizedBtn = screen.getByRole('button', { name: /Simultaneous/i });
    fireEvent.click(optimizedBtn);
    expect(setScenarioMock).toHaveBeenCalledWith('Optimized');
  });

  test('calls setCurrentMode when Actual Machine State dropdown value changes', () => {
    const setCurrentModeMock = vi.fn();
    render(
      <RecommendationPanel 
        recommendation={mockRecommendation}
        scenario="Standard"
        setScenario={vi.fn()}
        currentMode="Standard"
        setCurrentMode={setCurrentModeMock}
        isSimulating={true}
      />
    );

    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'Optimized' } });
    expect(setCurrentModeMock).toHaveBeenCalledWith('Optimized');
  });

  test('handles Acknowledge button dispatch click', () => {
    render(
      <RecommendationPanel 
        recommendation={mockRecommendation}
        scenario="Standard"
        setScenario={vi.fn()}
        currentMode="Standard"
        setCurrentMode={vi.fn()}
        isSimulating={true}
      />
    );

    const ackBtn = screen.getByRole('button', { name: /Acknowledge & Adjust/i });
    fireEvent.click(ackBtn);
    expect(screen.getByText(/Actions Dispatched/i)).toBeInTheDocument();
  });
});
