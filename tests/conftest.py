"""
Pytest Conftest — Shared fixtures untuk seluruh test suite.

File ini akan berisi:
- Fixture untuk sample DataFrame (data telemetry kecil untuk testing)
- Fixture untuk loaded model (mock atau model kecil)
- Fixture untuk konfigurasi test
- Temporary directory fixtures untuk output test

Contoh:
    @pytest.fixture
    def sample_telemetry_df():
        \'\'\'DataFrame kecil berisi data telemetry untuk testing.\'\'\'
        return pd.DataFrame({
            "I_w_BLO_Weg": [0.5, 1.2, 0.8],
            "O_w_BLO_power": [100, 250, 150],
            "operation_type": [0, 1, 0],
        })

TODO: Implement shared test fixtures.
"""
