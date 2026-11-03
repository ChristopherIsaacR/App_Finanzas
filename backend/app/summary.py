"""Resumen comparativo desde la base de datos.
Uso (desde backend/):  python -m app.summary MSFT AAPL VOO [--rf 0.04]"""
import argparse

import pandas as pd

from app.analysis.indicators import rsi, sma
from app.analysis.risk import correlation_matrix, summarize
from app.data.repositories.market_repository import get_engine, init_db, load_prices


def main() -> None:
    p = argparse.ArgumentParser(description="Resumen de rendimiento, riesgo e indicadores.")
    p.add_argument("tickers", nargs="+")
    p.add_argument("--rf", type=float, default=0.0, help="Tasa libre de riesgo anual, p. ej. 0.04")
    args = p.parse_args()

    engine = get_engine()
    init_db(engine)
    filas, closes = {}, {}
    for t in args.tickers:
        df = load_prices(engine, t)
        if df.empty:
            print(f"[AVISO] {t}: sin datos. Ejecuta primero: python -m app.cli {t}")
            continue
        close = df["close"]
        closes[t.upper()] = close
        s = summarize(close, args.rf)
        s["rsi_14"] = float(rsi(close).iloc[-1])
        s["vs_sma200"] = "sobre" if len(close) >= 200 and close.iloc[-1] > sma(close, 200).iloc[-1] else "bajo"
        filas[t.upper()] = s

    if not filas:
        return
    tabla = pd.DataFrame(filas).T
    for c in ["rendimiento_acumulado", "rendimiento_anual", "volatilidad_anual", "max_drawdown"]:
        tabla[c] = tabla[c].astype(float).map("{:.1%}".format)
    tabla["sharpe"] = tabla["sharpe"].astype(float).map("{:.2f}".format)
    tabla["rsi_14"] = tabla["rsi_14"].astype(float).map("{:.0f}".format)
    print("\n", tabla.to_string())
    if len(closes) > 1:
        print("\nCorrelación de rendimientos diarios:\n", correlation_matrix(closes).round(2).to_string())
    print("\nNota: datos históricos informativos. No son una recomendación de inversión.")


if __name__ == "__main__":
    main()
