import aiohttp
from bs4 import BeautifulSoup

from ._client import Client


class ScraperHandler(Client):
    """
    A class that handles scraping webpages.


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "Scraper"

    async def fetch(self):
        """
        Asynchronously scrapes a webpage and retrieves
        the content specified by the scraper_page_url
        and scraper_page_id attributes.

        :return: The content of the webpage as a string,
        formatted using BeautifulSoup.
        If the scraper_page_id is not specified,
        the entire webpage is returned.

        :rtype: str
        """
        if self.enabled and self.url:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.url, headers=headers, timeout=10
                ) as response:
                    response.raise_for_status()
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    if not self.url_element:
                        return soup.prettify()
                    description_element = soup.select_one(self.url_element)
                    return description_element.get_text() if description_element else ""

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
