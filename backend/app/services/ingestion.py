"""Flujo completo: descargar -> limpiar -> guardar."""
from sqlalchemy import Engine

from app.data.collectors.yahoo_collector import fetch_history, fetch_metadata
from app.data.processors.cleaner import clean_prices
from app.data.repositories.market_repository import save_prices


def ingest_ticker(engine: Engine, ticker: str, period: str = "5y") -> dict:
    raw = fetch_history(ticker, period=period)
    limpio, reporte = clean_prices(raw)
    meta = fetch_metadata(ticker)
    insertadas = save_prices(engine, ticker, limpio, source="yahoo", **meta)
    return {"ticker": ticker.upper(), "inserted": insertadas, "cleaning": reporte.as_dict()}
