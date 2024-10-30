#import websockets
from loguru import logger


class Client:

    def __init__(self, **kwargs):
        """
        Initializes the Client object
        with the given keyword arguments.

        :param kwargs: Variable length keyword arguments.
        :type kwargs: dict

        :return: None
        """

        logger.info("Initializing Client")
        get = kwargs.get
        self.name = get("name", None)
        self.enabled = get("enabled", True)
        self.library = get("library", None)
        self.instrument = get("instrument", None)
        self.format = get("format", None)
        self.url = get("url", None)
        self.url_element = get("url_element", None)
        self.api_key = get("api_key", None)
        self.api_category = get("api_category", None)
        self.ticker = get("ticker", "AAPL")
        self.stream = get("stream", False)
        self.websocket_url = get("websocket_url", None)
        self.client = None

    async def fetch(self):
        """
        Asynchronously fetches data from the source
        using the configured settings.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """

    async def get_news(self):
        """
        Asynchronously retrieves the latest news
        from various sources based on the configured
        settings.

        Returns:
            str: A string containing the concatenated
             results of the retrieved news sources.
        """

    # async def stream(self):
    #     """
    #     Asynchronously streams data from the source
    #     using the configured settings.

    #     Returns:
    #         str: A string containing the concatenated results
    #          of the retrieved data sources.
    #     """
    # async def stream(self):
    #     """
    #     Asynchronously streams data from the source
    #     using the configured settings.

    #     Returns:
    #         str: A string containing the concatenated results
    #          of the retrieved data sources.
    #     """

    #     if self.websocket_url is None:
    #         return
    #     with websockets.connect(self.websocket_url) as websocket:
    #         message = websocket.recv()
    #         logger.info(f"Received: {message}")
    #         yield message
