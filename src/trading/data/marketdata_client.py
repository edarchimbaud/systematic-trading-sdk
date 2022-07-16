"""
Client for the API https://marketdata.edarchimbaud.com
"""
from datetime import date
import os

import pandas as pd
import requests


class MarketDataClient:
    """
    Client for the API https://marketdata.edarchimbaud.com
    """

    def __init__(self):
        self.api_url = "https://marketdata.edarchimbaud.com"
        self.headers = {"Authorization": os.getenv("DATA_SECRET_KEY")}

    @staticmethod
    def __format_response(response):
        response_json = response.json()
        error = response_json["error"]
        if error is not None:
            raise Exception(error)
        data = response_json["data"]
        dfm = pd.DataFrame.from_dict(data)
        dfm.set_index(dfm.columns[0], inplace=True)
        return dfm

    def get_daily_borrowing_rates(self, day: date):
        """
        Get daily borrowing rates.

        Parameters
        ----------
            day: date
                Day of the rates to query.

        Returns
        -------
            DataFrame
                Borrowing rates.

            str
                Error message.
        """
        requests.get(
            f"{self.api_url}/daily/borrowing-rates",
            headers=self.headers,
            params={
                "day": day.isoformat(),
            },
        )

    def get_historical_prices(self, ticker: str) -> pd.DataFrame:
        """
        Get historical prices.

        Parameters
        ----------
            ticker: str
                Instrument ticker.

        Returns
        -------
            DataFrame
                Dataset data.
        """
        url = f"{self.api_url}/historical/prices"
        response = requests.get(
            url,
            params={
                "ticker": ticker,
            },
        )
        return self.__format_response(response)

    def get_instruments(self) -> pd.DataFrame:
        """
        Get instruments.

        Returns
        -------
            DataFrame
                Dataset data.
        """
        url = f"{self.api_url}/instruments"
        response = requests.get(
            url,
            params={},
        )
        return self.__format_response(response)
