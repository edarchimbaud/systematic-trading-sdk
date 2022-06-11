"""
Copyright edarchimbaud
"""
from datetime import date, timedelta

import pandas as pd
from tqdm import tqdm

from trading.models.market_data import MarketData
from trading.utils.contract import get_front_contract, get_next_contract


def test_get_front_contract(snapshot):
    """
    Test get_front_contract
    """
    def test(tickers: list, start_date: date, end_date: date):
        delta = end_date - start_date
        index = []
        data = []
        for i in tqdm(range(delta.days + 1)):
            day = start_date + timedelta(days=i)
            index.append(day)
            row = {}
            for ticker in tickers:
                front_ltd, front_ric = get_front_contract(day=day, ticker=ticker)
                row[f"{ticker}_ric"] = front_ric
                row[f"{ticker}_ltd"] = front_ltd
            data.append(row)
        dfm = pd.DataFrame(index=index, data=data)
        return dfm.to_string()
    tickers = ["ES", "NQ", "GC", "ZF", "ZN", "ZT"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    snapshot.assert_match(test(tickers, start_date, end_date), "output.yml")


def test_get_next_contract(snapshot):
    """
    Test get_next_contract
    """
    def test(tickers: list, start_date: date, end_date: date):
        delta = end_date - start_date
        index = []
        data = []
        for i in tqdm(range(delta.days + 1)):
            day = start_date + timedelta(days=i)
            index.append(day)
            row = {}
            for ticker in tickers:
                front_ltd, front_ric = get_next_contract(day=day, ticker=ticker)
                row[f"{ticker}_ric"] = front_ric
                row[f"{ticker}_ltd"] = front_ltd
            data.append(row)
        dfm = pd.DataFrame(index=index, data=data)
        return dfm.to_string()
    tickers = ["ES", "NQ", "GC", "ZF", "ZN", "ZT"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    snapshot.assert_match(test(tickers, start_date, end_date), "output.yml")


def test_should_roll_today(snapshot):
    """
    Test should_roll_today
    """
    market_data = MarketData()
    def test(tickers: list, start_date: date, end_date: date):
        delta = end_date - start_date
        index = []
        data = []
        for i in tqdm(range(delta.days + 1)):
            day = start_date + timedelta(days=i)
            index.append(day)
            row = {}
            for ticker in tickers:
                row[ticker] = market_data.should_roll_today(day=day, ticker=ticker)
            data.append(row)
        dfm = pd.DataFrame(index=index, data=data)
        return dfm.to_string()
    tickers = ["ES", "NQ", "GC", "ZF", "ZN", "ZT"]
    start_date = date(2022, 1, 1)
    end_date = date(2022, 6, 10)
    snapshot.assert_match(test(tickers, start_date, end_date), "output.yml")
