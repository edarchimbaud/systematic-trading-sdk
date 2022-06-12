"""
Copyright edarchimbaud
"""

from trading.models.market_impact import MarketImpact


def test_get_market_impact():
    """
    Test get_front_contract
    """
    market_impact = MarketImpact()
    assert market_impact.get("ES") == 7.955449482888177e-05


