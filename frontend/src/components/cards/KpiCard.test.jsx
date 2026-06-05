import React from 'react';
import { render, screen } from '@testing-library/react';
import KpiCard from './KpiCard';

describe('KpiCard Component', () => {
  test('renders title, value, and unit correctly', () => {
    render(<KpiCard title="Test Metric" value="42.5" unit="kW" type="power" />);
    
    expect(screen.getByText('Test Metric')).toBeInTheDocument();
    expect(screen.getByText('42.5')).toBeInTheDocument();
    expect(screen.getByText('kW')).toBeInTheDocument();
  });

  test('applies correct type class name', () => {
    const { container } = render(<KpiCard title="Test Metric" value="42.5" unit="kW" type="voltage" />);
    const cardElement = container.querySelector('.kpi-card');
    expect(cardElement).toHaveClass('voltage');
  });

  test('applies warning pulse animation class when isWarning is true', () => {
    const { container } = render(<KpiCard title="Test Metric" value="42.5" unit="kW" isWarning={true} />);
    const cardElement = container.querySelector('.kpi-card');
    expect(cardElement).toHaveClass('alert-pulse');
  });

  test('does not apply warning class when isWarning is false', () => {
    const { container } = render(<KpiCard title="Test Metric" value="42.5" unit="kW" isWarning={false} />);
    const cardElement = container.querySelector('.kpi-card');
    expect(cardElement).not.toHaveClass('alert-pulse');
  });
});
