"""
Copyright edarchimbaud
"""
from datetime import date
import pytest
from trading.data.constants import FUTURE_TYPE
from trading.models.backtester import Backtester
from trading.models.backtester_parameters import BacktesterParameters


def test_run():
    """
    Test run
    """
    params = BacktesterParameters()
    params.cash = 1e6
    params.tickers = []
    params.start_date = date(2022, 1, 1)
    params.end_date = date(2022, 6, 10)
    backtester = Backtester(params=params)
    with pytest.raises(Exception) as exception:
        backtester.run()
    assert str(exception.value) == "To be implemented in the child class"


