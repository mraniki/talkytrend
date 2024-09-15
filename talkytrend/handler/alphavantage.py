from alpha_vantage.alphaintelligence import AlphaIntelligence
from loguru import logger

from ._client import Client


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
            self.client = AlphaIntelligence(key=self.api_key, output_format="json")

    async def get_news(self):
        # TODO return cleaned news articles
        news = self.client.get_news_sentiment(limit=1)
        logger.debug("Data: {}", news[0])
        return news
