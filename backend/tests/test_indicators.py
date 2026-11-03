import numpy as np
import pandas as pd
import pytest

from app.analysis.indicators import bollinger, ema, macd, rsi, sma


def _serie(vals):
    return pd.Series(vals, index=pd.date_range("2024-01-01", periods=len(vals), freq="D"), dtype=float)


def test_sma():
    out = sma(_serie([1, 2, 3, 4, 5]), 3)
    assert np.isnan(out.iloc[1])
    assert out.iloc[2] == pytest.approx(2.0)
    assert out.iloc[4] == pytest.approx(4.0)


def test_ema_constante():
    assert ema(_serie([5] * 30), 10).iloc[-1] == pytest.approx(5.0)


def test_rsi_tendencia_alcista_es_100():
    assert rsi(_serie(range(1, 40)), 14).iloc[-1] == pytest.approx(100.0)


def test_rsi_tendencia_bajista_es_0():
    assert rsi(_serie(range(40, 1, -1)), 14).iloc[-1] == pytest.approx(0.0, abs=1e-6)


def test_rsi_rango():
    rng = np.random.default_rng(1)
    out = rsi(_serie(100 + rng.normal(0, 1, 200).cumsum()), 14).dropna()
    assert ((out >= 0) & (out <= 100)).all()


def test_macd_columnas_y_hist():
    out = macd(_serie(np.linspace(100, 150, 100)))
    assert list(out.columns) == ["macd", "signal", "hist"]
    assert (out["hist"] - (out["macd"] - out["signal"])).abs().max() < 1e-9


def test_bollinger_orden():
    rng = np.random.default_rng(2)
    b = bollinger(_serie(100 + rng.normal(0, 1, 60).cumsum())).dropna()
    assert (b["upper"] >= b["mid"]).all() and (b["mid"] >= b["lower"]).all()
