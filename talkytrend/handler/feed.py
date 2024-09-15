import aiohttp
import xmltodict
from loguru import logger

from ._client import Client


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
            self.client = "Feed"

    async def fetch(self):
        """
        Asynchronously fetches a news rss feed from the specified URL.

        :return: The formatted news feed as a string with an HTML link.
        :rtype: str or None
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=10) as response:
                    logger.debug("Fetching news from {}", self.url)
                    data = (
                        xmltodict.parse(await response.text())
                        .get("rss")
                        .get("channel")["item"][0]
                    )
                    title = data["title"]
                    link = data["link"]
                    return f"📰 <a href='{link}'>{title}</a>"
        except Exception as error:
            logger.error("Error occurred while fetching news: {}", error)
            return f"📰 {error}"

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """

        return await self.fetch()
