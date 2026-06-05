import React from 'react';
import { renderHook, act, waitFor } from '@testing-library/react';
import { TelemetryProvider, useTelemetry } from './TelemetryContext';

describe('TelemetryContext Integration', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  test('checks health endpoint on mount and handles online status', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({ ok: true });
      }
      return Promise.resolve({ ok: false });
    });

    const wrapper = ({ children }) => <TelemetryProvider>{children}</TelemetryProvider>;
    const { result } = renderHook(() => useTelemetry(), { wrapper });

    // Wait for health check to complete
    await waitFor(() => {
      expect(result.current.status).toBe('online');
    });

    expect(fetchSpy).toHaveBeenCalledWith('http://localhost:8000/health');
  });

  test('handles health check failure by setting offline status', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error('Network Error'));
    });

    const wrapper = ({ children }) => <TelemetryProvider>{children}</TelemetryProvider>;
    const { result } = renderHook(() => useTelemetry(), { wrapper });

    await waitFor(() => {
      expect(result.current.status).toBe('offline');
    });
  });

  test('toggles simulation and fetches recommendation from backend API', async () => {
    // Enable fake timers specifically for this test
    vi.useFakeTimers();

    const mockRecResponse = {
      ml_predicted_profile: 'Optimized',
      efficiency_score: 95.0,
      operational_risk_level: 'Low Risk',
      technical_alerts: ['Semua metrik normal'],
      primary_recommendation: 'Optimize operations.'
    };

    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation((url) => {
      if (url.includes('/health')) {
        return Promise.resolve({ ok: true });
      }
      if (url.includes('/simulate/telemetry')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            O_w_BLO_power: 1000,
            O_w_BHL_power: 1000,
            O_w_BHR_power: 1000,
            O_w_BRU_power: 1000,
            O_w_HR_power: 1000,
            O_w_HL_power: 1000,
            O_w_BLO_voltage: 220,
            O_w_BHL_voltage: 220,
            O_w_BHR_voltage: 220,
            O_w_BRU_voltage: 220,
            O_w_HR_voltage: 220,
            O_w_HL_voltage: 220,
            Timestamp: 1622505600
          })
        });
      }
      if (url.includes('/recommend')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockRecResponse)
        });
      }
      return Promise.resolve({ ok: false });
    });

    const wrapper = ({ children }) => <TelemetryProvider>{children}</TelemetryProvider>;
    const { result } = renderHook(() => useTelemetry(), { wrapper });

    // Since we are in fake timers, let's advance time to let health check fetch run and complete
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.status).toBe('online');

    // Start simulation
    act(() => {
      result.current.toggleSimulation();
    });

    expect(result.current.isSimulating).toBe(true);

    // Let the first recommendation fetch promise resolve
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.recommendation).toEqual(mockRecResponse);

    // Verify stats calculation
    expect(result.current.stats.powerEfficiency).toBe(0.95);
    expect(result.current.stats.totalPower).toBeGreaterThan(0);
    expect(result.current.stats.avgVoltage).toBeGreaterThan(0);
    expect(result.current.chartData.length).toBe(1);

    // Advance 2 seconds to trigger another step
    await act(async () => {
      await vi.advanceTimersByTimeAsync(2000);
    });

    expect(result.current.chartData.length).toBe(2);

    // Stop simulation
    act(() => {
      result.current.toggleSimulation();
    });

    expect(result.current.isSimulating).toBe(false);

    vi.useRealTimers();
  });
});
