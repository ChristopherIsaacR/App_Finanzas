"""Descarga de datos desde Yahoo Finance (yfinance).

Aviso: yfinance es una herramienta comunitaria, no oficial. Úsala para
investigación y uso personal; no son cotizaciones oficiales para operar.
Para un producto público necesitarás un proveedor con licencia comercial.
"""
import pandas as pd


class DataNotFoundError(Exception):
    pass


def fetch_history(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    import yfinance as yf  # import local: facilita pruebas sin red

    df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
    if df is None or df.empty:
        raise DataNotFoundError(f"Sin datos para '{ticker}'. Revisa el símbolo.")
    return df


def fetch_metadata(ticker: str) -> dict:
    """Nombre, moneda y tipo de instrumento. Si falla, devuelve un dict vacío."""
    try:
        import yfinance as yf

        info = yf.Ticker(ticker).info
        return {
            "name": info.get("longName") or info.get("shortName"),
            "currency": info.get("currency"),
            "asset_type": info.get("quoteType"),
        }
    except Exception:
        return {}
