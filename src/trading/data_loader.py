"""
Data loader module.
"""
from datetime import date
import os

import pandas as pd
from .datasets import MarketDataClient


def load_futures_chain(ticker: str, asofdate: date) -> pd.DataFrame:
    """
    Get futures chain

    Parameters
    ----------
        ticker: str
            Future ticker.

        asofdate: date
            Current date. Will return only the live futures.
    """
    file_path = os.path.join(
        os.getenv("HOME"),
        ".trading",
        "data",
        "futures",
        ticker,
        f"chain.{date.today()}.csv",
    )
    if os.path.exists(file_path):
        chain = pd.read_csv(file_path, index_col="RIC")
    else:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        chain, _ = MarketDataClient().get_expiry_calendar(ticker)
        chain.set_index("RIC", drop=True, inplace=True)
        chain.to_csv(file_path, index=True, sep=",")
    chain.FTD = pd.to_datetime(chain.FTD)
    chain.LTD = pd.to_datetime(chain.LTD)
    index = pd.to_datetime(chain.LTD) >= asofdate
    chain = chain.loc[index, :]
    return chain


def load_futures_hist_prices(ticker: str) -> pd.DataFrame:
    """
    Load futures history prices.

    Parameters
    ----------
        ticker: str
            Future ticker.
    """
    file_path = os.path.join(
        os.getenv("HOME"),
        ".trading",
        "data",
        "futures",
        ticker,
        f"hist_prices.{date.today()}.csv",
    )
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col="Date")
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return MarketDataClient().get_historical_prices(ticker)


def load_futures_meta(ticker: str) -> dict:
    """
    Load futures meta

    Parameters
    ----------
        ticker: str
            Future ticker.

    Returns
    -------
        dict: Future meta data
    """
    client = MarketDataClient()
    futures, _ = client.get_tickers()
    return futures[ticker]
