"""
Copyright edarchimbaud
"""
from datetime import date, timedelta

import pandas as pd

from trading.models.contract import Contract
from trading.models.market_data import MarketData


def test_front_contract(snapshot):
    """
    Test front_contract
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
            front_contract, front_ltd = Contract(day=day, ticker=ticker).front_contract
            row[f"{ticker}_ric"] = front_contract.ric
            row[f"{ticker}_ltd"] = front_ltd
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_next_contract(snapshot):
    """
    Test next_contract
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
            next_contract, next_ltd = Contract(day=day, ticker=ticker).next_contract
            row[f"{ticker}_ric"] = next_contract.ric
            row[f"{ticker}_ltd"] = next_ltd
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
