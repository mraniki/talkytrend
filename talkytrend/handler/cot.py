from loguru import logger
import cot_reports as cot

from .client import Client


class CotHandler(Client):
    """

    COT report client


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "CoT"