import requests
from bs4 import BeautifulSoup

from .client import Client


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

    async def scrape_page(self):
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
        try:
            if self.enable_scraper and self.scraper_page_url:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(self.scraper_page_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                if not self.scraper_page_id:
                    return soup.prettify()
                description_element = soup.select(self.scraper_page_id)
                return description_element[0].get_text()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
