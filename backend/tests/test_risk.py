import numpy as np
import pandas as pd
import pytest

from app.analysis.risk import (annualized_return, annualized_volatility, correlation_matrix,
                               cumulative_return, drawdown_series, max_drawdown, sharpe_ratio)


def _serie(vals, start="2024-01-01"):
    return pd.Series(vals, index=pd.date_range(start, periods=len(vals), freq="D"), dtype=float)


def test_max_drawdown():
    s = _serie([100, 120, 60, 90])
    assert max_drawdown(s) == pytest.approx(-0.5)
    assert drawdown_series(s).iloc[1] == 0


def test_rendimiento_acumulado():
    assert cumulative_return(_serie([100, 150])) == pytest.approx(0.5)


def test_cagr_duplicar_en_dos_anios():
    s = pd.Series([100.0, 200.0], index=pd.to_datetime(["2020-01-01", "2022-01-01"]))
    assert annualized_return(s) == pytest.approx(0.414, abs=0.01)


def test_volatilidad_cero_si_rendimiento_constante():
    s = _serie(100 * 1.01 ** np.arange(50))
    assert annualized_volatility(s) == pytest.approx(0.0, abs=1e-9)


def test_sharpe_nan_sin_variacion():
    assert np.isnan(sharpe_ratio(_serie([100.0] * 20)))


def test_correlacion_consigo_misma():
    rng = np.random.default_rng(3)
    a = _serie(100 + rng.normal(0, 1, 100).cumsum() + 50)
    m = correlation_matrix({"A": a, "B": a * 2})
    assert m.loc["A", "B"] == pytest.approx(1.0)
