from alpha_vantage.alphaintelligence import AlphaIntelligence

# from alpha_vantage.alphavantage import AlphaVantage
from .client import Client


class AlphavantageHandler(Client):
    """
    AlphaVantage API client

    documentation: https://www.alphavantage.co/documentation/
    and https://github.com/RomelTorres/alpha_vantage

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:

            # Initialize the AlphaVantage Class with default values
            self.client = AlphaIntelligence(key=self.api_key)
            # if self.api_category is None
            #     self.api_category = "topnews"

    async def fetch(self):
        # TODO
        return self.client.get_news_sentiment(limit=1)
