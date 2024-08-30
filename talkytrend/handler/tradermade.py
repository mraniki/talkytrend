import tradermade as tm
from loguru import logger

from .client import Client


class TradermadeHandler(Client):
    """
    Tradermade API client
    documentation: https://github.com/tradermade/Python-SDK
    or https://tradermade.com/tutorials/python-sdk-for-forex-data


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "tradermade"
            logger.info("Initializing Tradermade")
            tm.set_rest_api_key(self.api_key)

    async def fetch(self):
        """ """
        # TODO
        return tm.live(currency="EURUSD,GBPUSD", fields=["bid", "mid", "ask"])
