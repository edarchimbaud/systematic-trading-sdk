"""
Copyright edarchimbaud
"""
from datetime import date

from trading.utils.dates import is_weekend


def test_is_weekend():
    """
    Test is_weekend
    """
    assert ~is_weekend(date(2022, 6, 10))
    assert is_weekend(date(2022, 6, 11))
    assert is_weekend(date(2022, 6, 12))




    


