"""
Util func module.
"""
from datetime import datetime
import os
import pickle

import pandas as pd


def read_data(
    filepath: str, instrument: str, tz: str = "America/New_York"
) -> pd.DataFrame:
    """
    Read data from csv file.

    Parameters
    ----------
        filepath : str
            Filepath.

        instrument : str
            Instrument.

        tz : str
            Timezone.

    Returns
    -------
        pd.DataFrame: Market data.

    """
    dfm = pd.read_csv(filepath, parse_dates=True, sep=",")
    dfm.set_index("Date", inplace=True)
    dfm.index = pd.to_datetime(dfm.index)
    dfm.index = dfm.index + pd.DateOffset(hours=16)
    dfm.index = dfm.index.tz_localize(tz)  # US/Eastern, UTC
    dfm = dfm.loc[dfm.Instrument == instrument, :]  # pylint: disable=no-member
    return dfm


def read_ohlcv_csv(filepath: str, adjust: bool = True, tz: str = "America/New_York"):
    """
    Read ohlcv data from csv file.

    Parameters
    ----------
        filepath : str
            Filepath.

        adjust : bool
            Adjust timezone.

        tz : str
            Timezone.

    Returns
    -------
        pd.DataFrame: OHLCV data.
    """
    dfm = pd.read_csv(filepath, header=0, parse_dates=True, sep=",", index_col=0)
    dfm.index = dfm.index + pd.DateOffset(hours=16)
    dfm.index = dfm.index.tz_localize(tz)  # US/Eastern, UTC
    # dfm.index = pd.to_datetime(dfm.index)
    if adjust:
        dfm["Open"] = dfm["Adj Close"] / dfm["Close"] * dfm["Open"]
        dfm["High"] = dfm["Adj Close"] / dfm["Close"] * dfm["High"]
        dfm["Low"] = dfm["Adj Close"] / dfm["Close"] * dfm["Low"]
        dfm["Volume"] = dfm["Adj Close"] / dfm["Close"] * dfm["Volume"]
        dfm["Close"] = dfm["Adj Close"]

    dfm = dfm[["Open", "High", "Low", "Close", "Volume"]]
    return dfm


def read_intraday_bar_pickle(filepath: str, syms: list, tz: str = "America/New_York"):
    """
    Read intraday bar data from pickle file.

    Parameters
    ----------
        filepath : str
            Filepath.

        syms : list
            Symbols.

        tz : str
            Timezone.

    Returns
    -------
        pd.DataFrame: Intraday bar data.
    """
    dict_hist_data = {}
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            dict_hist_data = pickle.load(f)
    dict_ret = {}
    for sym in syms:
        try:
            dfm = dict_hist_data[sym]
            dfm.index = dfm.index.tz_localize(tz)  # # US/Eastern, UTC
            dict_ret[sym] = dfm
        except:  # pylint: disable=bare-except
            pass
    return dict_ret


def read_tick_data_txt(
    filepath: str, remove_bo: bool = True, tz: str = "America/New_York"
):
    """
    Read tick data from txt file.
    filename = yyyymmdd.txt

    Parameters
    ----------
        filepath : str
            Filepath.

        remove_bo : bool
            Remove backorder.

        tz : str
            Timezone.

    Returns
    -------
        pd.DataFrame: Tick data.
    """
    asofdate = filepath.split("/")[-1].split(".")[0]
    data = pd.read_csv(filepath, sep=",", header=None)
    data.columns = [
        "Time",
        "ProcessTime",
        "Ticker",
        "Type",
        "BidSize",
        "Bid",
        "Ask",
        "AskSize",
        "Price",
        "Size",
    ]
    data = data[
        ["Time", "Ticker", "Type", "BidSize", "Bid", "Ask", "AskSize", "Price", "Size"]
    ]
    if remove_bo:
        data = data[data.Type.str.contains("TickType.TRADE")]
    data.Time = data.Time.apply(
        lambda t: datetime.strptime(f"{asofdate} {t}", "%Y%m%d %H:%M:%S.%f")
    )
    data.set_index("Time", inplace=True)
    data.index = data.index.tz_localize(tz)  # # US/Eastern, UTC
    dg = data.groupby("Ticker")
    dict_ret = {}
    for sym, dgf in dg:
        dgf = dgf[~dgf.index.duplicated(keep="last")]
        dict_ret[sym] = dgf
    return dict_ret


def save_one_run_results(
    output_dir: str,
    equity: pd.DataFrame,
    df_positions: pd.DataFrame,
    df_trades: pd.DataFrame,
    batch_tag: tuple = None,
):
    """
    Save one run results.

    Parameters
    ----------
        output_dir : str
            Output directory.

        equity : pd.DataFrame
            Equity.

        df_positions : pd.DataFrame
            Positions.

        df_trades : pd.DataFrame
            Trades.

        batch_tag : tuple
            Batch tag.
    """
    df_positions.to_csv(
        "{}{}{}{}".format(
            output_dir, "/positions_", batch_tag if batch_tag else "", ".csv"
        )
    )
    df_trades.to_csv(
        "{}{}{}{}".format(
            output_dir, "/trades_", batch_tag if batch_tag else "", ".csv"
        )
    )
    equity.to_csv(
        "{}{}{}{}".format(
            output_dir, "/equity_", batch_tag if batch_tag else "", ".csv"
        )
    )
