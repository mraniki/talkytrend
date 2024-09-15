import aiohttp
from loguru import logger

from ._client import Client


class MarketauxHandler(Client):
    """
    Marketaux client
    documentation: https://www.marketaux.com/documentation

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "Marketaux"
            logger.info("Initializing Marketaux with self.url={}", self.url)

    async def get_news(self):
        """
        Asynchronously retrieves news articles from the Marketaux endpoint
        based on the specified url.

        :return: A string containing HTML formatted news summaries
        linked to their respective URLs.
        Returns None if an error occurs while retrieving the news.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, timeout=10) as response:
                logger.debug("Fetching events from {}", self.url)
                response.raise_for_status()
                data = await response.json()

                news_articles = []
                for article in data["data"]:
                    url = article["url"]
                    title = article["title"]
                    # sentiment = article["entities"][0]["sentiment_score"]
                    article_summary = f"<a href='{url}'>{title}</a><br>"

                    news_articles.append(article_summary)

                return "<br><br>".join(news_articles)
