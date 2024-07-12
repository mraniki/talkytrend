from loguru import logger


class TalkyTrendClient:

    def __init__(self, **kwargs):
        """
        Initialize the TalkyTrend object

        Args:
            None
        """

        logger.info("Initializing Client")
        self.name = kwargs.get("name", None)
        self.enabled = kwargs.get("enabled", True)
        self.library = kwargs.get("library", None)

        self.instrument = kwargs.get("instrument", None)
        self.format = kwargs.get("format", None)
        self.url = kwargs.get("url", None)
        self.date = kwargs.get("date", None)
        self.api_key = kwargs.get("api_key", None)
        self.category = kwargs.get("category", None)
        self.scraper_page_id = kwargs.get("scraper_page_id", None)

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

