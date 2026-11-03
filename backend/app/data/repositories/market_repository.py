"""Acceso a la base de datos. SQLite por defecto; PostgreSQL con DATABASE_URL."""
import datetime as dt

import pandas as pd
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from app.core.config import DATA_DIR, settings
from app.models.db import Base, Instrument, PriceDaily


def get_engine(url: str | None = None) -> Engine:
    url = url or settings.database_url
    if url.startswith("sqlite"):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    return create_engine(url, future=True)


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def save_prices(engine: Engine, ticker: str, df: pd.DataFrame, source: str = "yahoo",
                name: str | None = None, currency: str | None = None,
                asset_type: str | None = None) -> int:
    """Guarda solo las fechas nuevas. Devuelve cuántas filas insertó."""
    ticker = ticker.upper()
    with Session(engine) as s:
        inst = s.scalar(select(Instrument).where(Instrument.ticker == ticker))
        if inst is None:
            inst = Instrument(ticker=ticker, name=name, currency=currency, asset_type=asset_type)
            s.add(inst)
            s.flush()
        existentes = set(s.scalars(select(PriceDaily.date).where(PriceDaily.instrument_id == inst.id)))
        ahora = dt.datetime.now(dt.timezone.utc)
        nuevas = [
            PriceDaily(instrument_id=inst.id, date=fecha.date(), open=float(r.open), high=float(r.high),
                       low=float(r.low), close=float(r.close), volume=int(r.volume),
                       source=source, fetched_at=ahora)
            for fecha, r in df.iterrows() if fecha.date() not in existentes
        ]
        s.add_all(nuevas)
        s.commit()
        return len(nuevas)


def load_prices(engine: Engine, ticker: str) -> pd.DataFrame:
    """Devuelve el historial como DataFrame indexado por fecha."""
    with Session(engine) as s:
        rows = s.execute(
            select(PriceDaily.date, PriceDaily.open, PriceDaily.high, PriceDaily.low,
                   PriceDaily.close, PriceDaily.volume)
            .join(Instrument).where(Instrument.ticker == ticker.upper())
            .order_by(PriceDaily.date)
        ).all()
    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")
