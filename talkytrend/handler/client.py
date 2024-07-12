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

        self.assets = kwargs.get("assets", None)
        self.format = kwargs.get("format", None)
        self.yfinance_ticker_reference = kwargs.get("yfinance_ticker_reference", None)
        self.economic_calendar = kwargs.get("economic_calendar", None)
        self.fomc_decision_date = kwargs.get("fomc_decision_date", None)
        self.live_tv = kwargs.get("live_tv_url", None)
        self.feed_url = kwargs.get("feed_url", None)
        self.scraper_page_url = kwargs.get("scraper_page_url", None)
        self.scraper_page_id = kwargs.get("scraper_page_id", None)

        # self.api_key = kwargs.get("finnhub_api_key", None)
        # self.finnhub_news_category = kwargs.get("finnhub_news_category", None)

        self.client = None

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """
