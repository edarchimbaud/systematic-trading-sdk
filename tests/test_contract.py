"""
Copyright edarchimbaud
"""

# from trading.models.contract import get_expiry_calendar, ric_exists, Contract


# def test_get_expiry_calendar():
#     """
#     Test get_expiry_calendar
#     """
#     ticker = "ES"
#     row = get_expiry_calendar(ticker).iloc[0]
#     assert Contract(ric=row.RIC).ticker == ticker


# def test_ric_exists():
#     """
#     Test ric_exists
#     """
#     ticker = "ES"
#     row = get_expiry_calendar(ticker).iloc[0]
#     assert ric_exists(row.RIC)
#     wong_ric = "-" + row.RIC
#     assert ~ric_exists(wong_ric)
