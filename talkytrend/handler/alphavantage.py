from alphaVantageAPI import AlphaVantage

from .client import Client


class AlphavantageHandler(Client):
    """
    AlphaVantage API client


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
            self.client = AlphaVantage(
                api_key=self.api_key,
                premium=False,
                output_size="compact",
                datatype="json",
                export=False,
                export_path="~/av_data",
                output="csv",
                clean=False,
                proxy={},
            )

    async def fetch(self):
        pass
