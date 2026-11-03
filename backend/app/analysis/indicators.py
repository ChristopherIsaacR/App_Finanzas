"""Indicadores técnicos. Todas las funciones reciben pandas Series/DataFrame."""
import pandas as pd


def sma(close: pd.Series, period: int = 20) -> pd.Series:
    return close.rolling(window=period).mean()


def ema(close: pd.Series, period: int = 20) -> pd.Series:
    return close.ewm(span=period, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """RSI con suavizado de Wilder. Un RSI < 30 NO es señal automática de compra."""
    delta = close.diff()
    ganancias = delta.clip(lower=0)
    perdidas = -delta.clip(upper=0)
    prom_g = ganancias.ewm(alpha=1 / period, adjust=False).mean()
    prom_p = perdidas.ewm(alpha=1 / period, adjust=False).mean()
    rs = prom_g / prom_p
    return 100 - (100 / (1 + rs))


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    linea = ema(close, fast) - ema(close, slow)
    senal = linea.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({"macd": linea, "signal": senal, "hist": linea - senal})


def bollinger(close: pd.Series, period: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    media = sma(close, period)
    desv = close.rolling(window=period).std()
    return pd.DataFrame({"mid": media, "upper": media + num_std * desv, "lower": media - num_std * desv})


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range. Requiere columnas high, low, close."""
    cierre_prev = df["close"].shift(1)
    tr = pd.concat([df["high"] - df["low"],
                    (df["high"] - cierre_prev).abs(),
                    (df["low"] - cierre_prev).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()
