import pandas as pd

from app.data.repositories.market_repository import get_engine, init_db, load_prices, save_prices


def _df(dias):
    idx = pd.to_datetime(dias)
    return pd.DataFrame({"open": 10.0, "high": 11.0, "low": 9.0, "close": 10.5, "volume": 100}, index=idx)


def test_guardar_y_no_duplicar(tmp_path):
    e = get_engine(f"sqlite:///{tmp_path/'t.db'}")
    init_db(e)
    assert save_prices(e, "msft", _df(["2024-01-02", "2024-01-03"])) == 2
    # Segunda descarga con una fecha repetida y una nueva
    assert save_prices(e, "MSFT", _df(["2024-01-03", "2024-01-04"])) == 1
    df = load_prices(e, "MSFT")
    assert len(df) == 3
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
