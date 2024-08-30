# from alpha_vantage.alphaintelligence import AlphaIntelligence
from alpha_vantage.alphavantage import AlphaVantage

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
            self.client = AlphaVantage(key=self.api_key)

    async def fetch(self):
        # TODO
        pass
