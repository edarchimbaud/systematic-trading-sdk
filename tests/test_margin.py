"""
Copyright edarchimbaud
"""
from datetime import date, timedelta

import pandas as pd
from trading.models.margin import Margin


def test_overnight_initial_future(snapshot):
    """
    Test overnight_initial_future
    """
    tickers = ["ES", "NQ", "GC", "ZF", "ZN", "ZT"]
    start_date = date(2021, 12, 1)
    end_date = date(2022, 2, 1)
    margin = Margin()
    delta = end_date - start_date
    index = []
    data = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        index.append(day)
        row = {}
        for ticker in tickers:
            row[ticker] = margin.overnight_initial_future(ticker=ticker, day=day)
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_overnight_maintenance_future(snapshot):
    """
    Test overnight_maintenance_future
    """
    tickers = ["ES", "NQ", "GC", "ZF", "ZN", "ZT"]
    start_date = date(2021, 12, 1)
    end_date = date(2022, 2, 1)
    margin = Margin()
    delta = end_date - start_date
    index = []
    data = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        index.append(day)
        row = {}
        for ticker in tickers:
            row[ticker] = margin.overnight_maintenance_future(ticker=ticker, day=day)
        data.append(row)
    dfm = pd.DataFrame(index=index, data=data)
    snapshot.assert_match(dfm.to_string(), "output.yml")
