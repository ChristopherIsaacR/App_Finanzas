import pandas as pd
import pytest

from app.data.processors.cleaner import clean_prices


def _df():
    idx = pd.to_datetime(["2024-01-03", "2024-01-02", "2024-01-02", "2024-01-04", "2024-01-05"])
    idx = idx.tz_localize("America/New_York")
    return pd.DataFrame({
        "Open": [10, 10, 11, 12, -1], "High": [11, 11, 12, 13, 5],
        "Low": [9, 9, 10, 11, 0.5], "Close": [10.5, 10.2, 11.5, None, 2],
        "Volume": [100, 200, 300, 400, 500]}, index=idx)


def test_limpieza_basica():
    out, rep = clean_prices(_df())
    assert out.index.tz is None
    assert out.index.is_monotonic_increasing
    assert not out.index.duplicated().any()
    assert rep.duplicates_removed == 1
    assert rep.missing_removed == 1       # Close = None
    assert rep.non_positive_removed == 1  # Open = -1
    assert rep.rows_out == len(out) == 2


def test_columnas_faltantes():
    with pytest.raises(ValueError):
        clean_prices(pd.DataFrame({"Close": [1]}, index=pd.to_datetime(["2024-01-01"])))
