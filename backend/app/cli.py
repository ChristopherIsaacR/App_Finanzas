"""Uso (desde la carpeta backend/):  python -m app.cli MSFT AAPL VOO --period 5y"""
import argparse

from app.core.config import settings
from app.data.collectors.yahoo_collector import DataNotFoundError
from app.data.repositories.market_repository import get_engine, init_db, load_prices
from app.services.ingestion import ingest_ticker


def main() -> None:
    p = argparse.ArgumentParser(description="Descarga y guarda precios históricos.")
    p.add_argument("tickers", nargs="+", help="Símbolos, p. ej. MSFT AAPL VOO")
    p.add_argument("--period", default=settings.default_period, help="1y, 5y, max...")
    args = p.parse_args()

    engine = get_engine()
    init_db(engine)
    for t in args.tickers:
        try:
            r = ingest_ticker(engine, t, args.period)
            df = load_prices(engine, t)
            print(f"[OK] {r['ticker']}: +{r['inserted']} filas nuevas | total {len(df)} "
                  f"({df.index.min().date()} a {df.index.max().date()}) | limpieza: {r['cleaning']}")
        except DataNotFoundError as e:
            print(f"[ERROR] {e}")
        except Exception as e:  # red caída, símbolo inválido, etc.
            print(f"[ERROR] {t}: {e}")


if __name__ == "__main__":
    main()
