"""
Copyright edarchimbaud
"""
from datetime import date
from trading.data.client import Client


def test_get_daily_factor_carry_bond(snapshot):
    """
    Test get_daily_factor with name="carry/bond"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="carry/bond",
        ticker="JGB",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_carry_commodity(snapshot):
    """
    Test get_daily_factor with name="carry/commodity"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="carry/commodity",
        ticker="GC",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_carry_currency(snapshot):
    """
    Test get_daily_factor with name="carry/currency"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="carry/currency",
        ticker="BP",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_carry_equity(snapshot):
    """
    Test get_daily_factor with name="carry/equity"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="carry/equity",
        ticker="ES",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_cot(snapshot):
    """
    Test get_daily_factor with name="cot"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="cot", ticker="CL", start_date=date(2022, 1, 1), end_date=date(2022, 3, 31)
    )
    snapshot.assert_match(dfm.iloc[:800, :].to_string(), "output.yml")


def test_get_daily_factor_currency(snapshot):
    """
    Test get_daily_factor with name="currency"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="currency",
        ticker="CGB",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_nav_long(snapshot):
    """
    Test get_daily_factor with name="nav/long"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="nav/long",
        ticker="ES",
        start_date=date(2020, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_nav_short(snapshot):
    """
    Test get_daily_factor with name="nav/short"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="nav/short",
        ticker="ES",
        start_date=date(2020, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_news_headlines(snapshot):
    """
    Test get_daily_factor with name="news/headlines"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="news/headlines",
        ticker="ES",
        start_date=date(2022, 6, 9),
        end_date=date(2022, 6, 10),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_news_stories(snapshot):
    """
    Test get_daily_factor with name="news/stories"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="news/stories",
        ticker="ES",
        start_date=date(2022, 6, 9),
        end_date=date(2022, 6, 10),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_roll_return(snapshot):
    """
    Test get_daily_factor with name="roll-return"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="roll-return",
        ticker="ES",
        start_date=date(2022, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_factor_splits(snapshot):
    """
    Test get_daily_factor with name="splits"
    """
    client = Client()
    dfm, _ = client.get_daily_factor(
        name="splits",
        ticker="ES",
        start_date=date(2020, 1, 1),
        end_date=date(2022, 3, 31),
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")


def test_get_daily_ohlcv(snapshot):
    """
    Test get_daily_ohlcv
    """
    client = Client()
    dfm, _ = client.get_daily_ohlcv(
        ric="GCJ2^2", start_date=date(2022, 1, 1), end_date=date(2022, 3, 31)
    )
    snapshot.assert_match(dfm.to_string(), "output.yml")
