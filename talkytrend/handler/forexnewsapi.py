import aiohttp
from loguru import logger

from ._client import Client


class ForexnewsapiHandler(Client):
    """
    forexnewsapi client

    docs: https://forexnewsapi.com/documentation

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "Forexnewsapi"
            logger.info("Initializing ForexnewsapiHandler with self.url={}", self.url)

    async def get_news(self):
        """
        Asynchronously retrieves news articles from the Forexnewsapi endpoint

        :return: A string containing HTML formatted news summaries
        linked to their respective URLs.
        Returns None if an error occurs while retrieving the news.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, timeout=10) as response:
                logger.debug("Fetching events from {}", self.url)
                response.raise_for_status()
                data = await response.json()
                logger.debug("Data: {}", data)
                news_articles = []
                for article in data["data"]:
                    news_url = article["news_url"]
                    title = article["title"]
                    text = article["text"]
                    sentiment = article["sentiment"]
                    article_summary = (
                        f"<a href='{news_url}'>{title}</a><br>"
                        f"{text}<br>"
                        f"Sentiment: {sentiment}"
                    )

                    news_articles.append(article_summary)
                logger.debug("news_articles: {}", news_articles)
                # return "<br><br>".join(news_articles)
                return "<br><br>".join([article_summary for _ in data["data"]])
