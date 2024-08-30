import aiohttp
from loguru import logger

from .client import Client


class ForexnewsapiHandler(Client):
    """
    forexnewsapi API client


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

    async def fetch(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, timeout=10) as response:
                logger.debug("Fetching events from {}", self.url)
                response.raise_for_status()
                data = await response.json()

                news_articles = []
                for article in data["data"]:
                    news_url = article["news_url"]
                    title = article["title"]
                    text = article["text"]
                    sentiment = article["sentiment"]

                    # Process the article data here
                    # For example, you can format the article data into a string
                    article_summary = (
                        f"<a href='{news_url}'>{title}</a><br>"
                        f"{text}<br>"
                        f"Sentiment: {sentiment}"
                    )

                    news_articles.append(article_summary)

                # Join the news articles into a single string
                news_summaries = "<br><br>".join(news_articles)

                return news_summaries
