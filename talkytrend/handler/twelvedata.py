from loguru import logger
from twelvedata import TDClient

from ._client import Client


class TwelvedataHandler(Client):
    """
    Twelvedata client
    docs: https://github.com/twelvedata/twelvedata-python


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = TDClient(apikey=self.api_key)
            logger.info("Initializing Twelvedata")

    async def get_news(self):
        """ """
        # TODO
