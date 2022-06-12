"""
Copyright edarchimbaud
"""
from datetime import date, timedelta

import pandas as pd

from trading.models.market_data import MarketData
from trading.utils.contract import get_front_contract, get_next_contract


def test_get_front_contract(snapshot):
    """
    Test get_front_contract
    """
    tickers = ["ES", "GC", "ZF"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    delta = end_date - start_date
    index = []
    data = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        index.append(day)
        row = {}
        for ticker in tickers:
            front_ltd, front_ric = get_front_contract(day=day, ticker=ticker)
            row[f"{ticker}_ric"] = front_ric
            row[f"{ticker}_ltd"] = front_ltd
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_next_contract(snapshot):
    """
    Test get_next_contract
    """
    tickers = ["ES", "GC", "ZF"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    delta = end_date - start_date
    index = []
    data = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        index.append(day)
        row = {}
        for ticker in tickers:
            front_ltd, front_ric = get_next_contract(day=day, ticker=ticker)
            row[f"{ticker}_ric"] = front_ric
            row[f"{ticker}_ltd"] = front_ltd
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_should_roll_today(snapshot):
    """
    Test should_roll_today
    """
    tickers = ["ES", "GC", "ZF"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    market_data = MarketData()
    delta = end_date - start_date
    index = []
    data = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        index.append(day)
        row = {}
        for ticker in tickers:
            row[ticker] = market_data.should_roll_today(day=day, ticker=ticker)
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")
