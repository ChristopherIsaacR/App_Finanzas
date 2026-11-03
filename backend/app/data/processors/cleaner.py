"""Limpieza y validación de precios históricos."""
from dataclasses import asdict, dataclass

import pandas as pd

PRICE_COLS = ["open", "high", "low", "close"]
REQUIRED = PRICE_COLS + ["volume"]


@dataclass
class CleaningReport:
    rows_in: int = 0
    rows_out: int = 0
    duplicates_removed: int = 0
    missing_removed: int = 0
    non_positive_removed: int = 0
    inconsistent_removed: int = 0

    def as_dict(self) -> dict:
        return asdict(self)


def clean_prices(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningReport]:
    """Normaliza columnas y fechas, elimina duplicados y filas inválidas."""
    report = CleaningReport(rows_in=len(df))
    out = df.copy()
    out.columns = [str(c).lower() for c in out.columns]

    faltantes = [c for c in REQUIRED if c not in out.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    out = out[REQUIRED]

    # Fechas: quitar zona horaria y dejar solo el día
    idx = pd.DatetimeIndex(pd.to_datetime(out.index))
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    out.index = idx.normalize()
    out.index.name = "date"

    dup = out.index.duplicated(keep="last")
    report.duplicates_removed = int(dup.sum())
    out = out[~dup]

    n = len(out)
    out = out.dropna(subset=PRICE_COLS)
    report.missing_removed = n - len(out)

    n = len(out)
    out = out[(out[PRICE_COLS] > 0).all(axis=1)]
    report.non_positive_removed = n - len(out)

    n = len(out)
    out = out[out["high"] >= out["low"]]
    report.inconsistent_removed = n - len(out)

    out["volume"] = out["volume"].fillna(0).astype("int64")
    out = out.sort_index()
    report.rows_out = len(out)
    return out, report
