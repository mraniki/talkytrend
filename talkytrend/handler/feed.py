import aiohttp
import xmltodict
from loguru import logger

from .client import Client


class FeedHandler(Client):
    """

    Feed Handler


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "feed"

    async def fetch_feed(self):
        """
        Asynchronously fetches a news rss feed from the specified URL.

        :return: The formatted news feed as a string with an HTML link.
        :rtype: str or None
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.feed_url, timeout=10) as response:
                logger.debug("Fetching news from {}", self.feed_url)
                data = (
                    xmltodict.parse(await response.text())
                    .get("rss")
                    .get("channel")["item"][0]
                )
                title = data["title"]
                link = data["link"]
                return f"📰 <a href='{link}'>{title}</a>"
