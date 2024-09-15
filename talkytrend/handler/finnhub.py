import finnhub

from ._client import Client


class FinnhubHandler(Client):
    """
    Finnhub API client

    documentation: https://finnhub.io/docs/api

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = finnhub.Client(api_key=self.api_key)
            self.websocket_url = f"wss://ws.finnhub.io?token={self.api_key}"

    async def get_news(self):
        """
        Asynchronously retrieves news articles from the Finnhub API
        based on the specified category and API key.

        :return: A string containing HTML formatted news summaries
        linked to their respective URLs.
        Returns None if an error occurs while retrieving the news.
        """

        news_data = self.client.general_news(self.api_category, min_id=0)
        # Create HTML formatted string for each news item
        news_summary_html = (
            f"<a href='{item['url']}' target='_blank'>{item['headline']}</a>"
            f"<br/><p>{item['summary']}</p>"
            for item in news_data
            if "headline" in item and "url" in item and "summary" in item
        )

        return "<br/>".join(news_summary_html)

    # async def stream(self):
    #     """
    #     Asynchronously streams data from the source
    #     using the configured settings.

    #     Returns:
    #         str: A string containing the concatenated results
    #          of the retrieved data sources.
    #     """
    #     # async with websockets.connect(self.websocket_url) as websocket:
    #     #     async for message in websocket:
    #     #         yield message

    #     with websockets.connect(self.websocket_url) as websocket:
    #         message = websocket.recv()
    #         logger.info(f"Received: {message}")
    #         yield message
