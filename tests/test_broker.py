"""
Copyright edarchimbaud
"""
from datetime import date
from trading.data.constants import FUTURE_TYPE
from trading.models.broker import Broker


def test_buy_future():
    """
    Test buy_future
    """
    ric = "GCJ2^2"
    broker = Broker(cash=1e6, live=False)
    broker.day = date(2022, 3, 7)
    broker.buy_future(ric=ric, contract_number=1)
    assert broker.positions["Cash"]["USD"] == 800378.2378610497
    assert broker.positions[FUTURE_TYPE][ric] == 1


def test_sell_future():
    """
    Test sell_future
    """
    ric = "GCJ2^2"
    broker = Broker(cash=1e6, live=False)
    broker.day = date(2022, 3, 7)
    broker.sell_future(ric=ric, contract_number=1)
    assert broker.positions["Cash"]["USD"] == 1199558.2378610496
    assert broker.positions[FUTURE_TYPE][ric] == -1


def test_close_future():
    """
    Test close_future
    """
    ric = "GCJ2^2"
    broker = Broker(cash=1e6, live=False)
    broker.day = date(2022, 3, 7)
    broker.buy_future(ric=ric, contract_number=1)
    broker.close_future(ric=ric)
    assert broker.positions["Cash"]["USD"] == 999936.4757220994
    assert broker.positions[FUTURE_TYPE][ric] == 0

def test_expire_future():
    """
    Test expire_future
    """
    ric = "GCJ2^2"
    broker = Broker(cash=1e6, live=False)
    broker.day = date(2022, 3, 7)
    broker.buy_future(ric=ric, contract_number=1)
    broker.expire_future(ric=ric)
    assert broker.positions["Cash"]["USD"] == 999936.4757220994
    assert broker.positions[FUTURE_TYPE][ric] == 0