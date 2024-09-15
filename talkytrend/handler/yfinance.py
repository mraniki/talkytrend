import yfinance as yf
from loguru import logger

from ._client import Client


class YfinanceHandler(Client):
    """

    YfinanceHandler


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "Yfinance"

    async def fetch(self, ticker=None):
        """
        Fetches the information for a given instrument from
        yahoo finance.

        Args:
            ticker_reference (str): The ticker symbol or
            reference of the instrument. Defaults to "MSFT".

        Returns:
            str: The formatted string containing the title
            and link of the latest news article for the instrument.
                 Returns None if there is no news available.
        """
        if ticker:
            logger.debug("Fetching news for {}", ticker)
            ticker = yf.Ticker(ticker)
            if news := ticker.news:
                title = news[0].get("title")
                link = news[0].get("link")
                return f"🗞️ <a href='{link}'>{title}</a>"

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """
        return await self.fetch(ticker=self.instrument)
