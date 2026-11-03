"""Rendimiento y riesgo a partir de una serie de precios de cierre (ajustados)."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252


def daily_returns(close: pd.Series) -> pd.Series:
    return close.pct_change().dropna()


def cumulative_return(close: pd.Series) -> float:
    return float(close.iloc[-1] / close.iloc[0] - 1)


def annualized_return(close: pd.Series) -> float:
    """Rendimiento anual compuesto (CAGR) según los días calendario reales."""
    years = (close.index[-1] - close.index[0]).days / 365.25
    if years <= 0:
        return float("nan")
    return float((close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1)


def annualized_volatility(close: pd.Series) -> float:
    return float(daily_returns(close).std() * np.sqrt(TRADING_DAYS))


def drawdown_series(close: pd.Series) -> pd.Series:
    """Caída porcentual respecto al máximo anterior (valores <= 0)."""
    return close / close.cummax() - 1


def max_drawdown(close: pd.Series) -> float:
    return float(drawdown_series(close).min())


def sharpe_ratio(close: pd.Series, risk_free: float = 0.0) -> float:
    """Sharpe anualizado. risk_free es la tasa anual libre de riesgo (0.04 = 4%).
    Usa una tasa acorde a la moneda del activo (USD vs MXN)."""
    exceso = daily_returns(close) - risk_free / TRADING_DAYS
    sd = exceso.std()
    if sd == 0 or np.isnan(sd):
        return float("nan")
    return float(exceso.mean() / sd * np.sqrt(TRADING_DAYS))


def correlation_matrix(closes: dict[str, pd.Series]) -> pd.DataFrame:
    """Correlación de rendimientos diarios entre instrumentos."""
    rets = pd.DataFrame({k: daily_returns(v) for k, v in closes.items()}).dropna()
    return rets.corr()


def summarize(close: pd.Series, risk_free: float = 0.0) -> dict:
    return {
        "rendimiento_acumulado": cumulative_return(close),
        "rendimiento_anual": annualized_return(close),
        "volatilidad_anual": annualized_volatility(close),
        "max_drawdown": max_drawdown(close),
        "sharpe": sharpe_ratio(close, risk_free),
    }
