"""
Copyright edarchimbaud
"""
from datetime import date

from trading.models.forex import Forex


def test_to_usd():
    """
    Test to_usd
    """
    forex = Forex()
    assert forex.to_usd(currency="AUD", day=date(2022, 6, 10)) == 0.7053180984624066
    assert forex.to_usd(currency="CAD", day=date(2022, 6, 10)) == 0.7822
    assert forex.to_usd(currency="CHF", day=date(2022, 6, 10)) == 1.0127
    assert forex.to_usd(currency="EUR", day=date(2022, 6, 10)) == 1.0518565267697486
    assert forex.to_usd(currency="GBP", day=date(2022, 6, 10)) == 1.231830500123183
    assert forex.to_usd(currency="HKD", day=date(2022, 6, 10)) == 0.12739
    assert forex.to_usd(currency="JPY", day=date(2022, 6, 10)) == 0.7438
    assert forex.to_usd(currency="USD", day=date(2022, 6, 10)) == 1
    assert forex.to_usd(currency="SGD", day=date(2022, 6, 10)) == 0.7201
