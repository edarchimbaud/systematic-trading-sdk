"""
Client for the API https://datasets.systematictrading.edarchimbaud.com
"""
import re

import pandas as pd
import requests


class Datasets:
    """
    Client for the API https://datasets.systematictrading.edarchimbaud.com
    """

    @staticmethod
    def __format_response(response: requests.Response) -> pd.DataFrame:
        response_json = response.json()
        error = response_json["error"]
        if error is not None:
            raise Exception(error)
        data = response_json["data"]
        dfm = pd.DataFrame.from_dict(data)
        dfm.set_index(dfm.columns[0], inplace=True)
        return dfm

    def get(self, url: str, ticker: str = None) -> pd.DataFrame:
        """
        Get dataset.

        Parameters
        ----------
            url: str
                URL of the dataset.
                /historical/actions
                /historical/balance-sheet/quarterly
                /historical/balance-sheet/yearly
                /historical/borrowing-rates/daily
                /historical/cashflow/yearly
                /historical/dividends
                /historical/financials/quarterly
                /historical/financials/yearly
                /historical/news
                /historical/prices/daily
                /historical/recommendations/daily
                /historical/splits
                /historical/statistics
                /instruments
                /live/prices

            ticker: str
                Ticker of the instrument.

        Returns
        -------
            DataFrame: Dataset data.

        Examples
        --------
            >>> from trading.datasets import Datasets
            >>> dfm = Datasets().get("/historical/prices/daily", "AAPL")
        """
        if re.search("^(/historical/|/live/)", url) and ticker is None:
            raise ValueError("Ticker is required for historical and live datasets.")
        if url == "/instruments" and ticker is not None:
            print("Ticker is not required for instruments dataset.")
        url_root = "https://datasets.systematictrading.edarchimbaud.com"
        response = requests.get(
            url_root + url,
            params={"ticker": ticker} if ticker else None,
        )
        return self.__format_response(response)
