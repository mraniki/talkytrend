from loguru import logger


class TalkyTrendClient:

    def __init__(self, **kwargs):
        """
        Initialize the TalkyTrend object

        Args:
            None
        """

        logger.info("Initializing Client")

        self.enable_signals = kwargs.get("enable_signals")
        self.assets = kwargs.get("assets")
        self.format = kwargs.get("format")

        self.enable_yfinance = kwargs.get("enable_yfinance")
        self.yfinance_ticker_reference = kwargs.get("yfinance_ticker_reference")

        self.enable_events = kwargs.get("enable_events")
        self.economic_calendar = kwargs.get("economic_calendar")
        self.fomc_decision_date = kwargs.get("fomc_decision_date")
        self.live_tv = kwargs.get("live_tv_url")

        self.enable_feed = kwargs.get("enable_feed")
        self.feed_url = kwargs.get("feed_url")

        self.enable_finnhub = kwargs.get("enable_finnhub")
        self.finnhub_api_key = kwargs.get("finnhub_api_key")
        self.finnhub_news_category = kwargs.get("finnhub_news_category")

        self.enable_scraper = kwargs.get("enable_scraper")
        self.scraper_page_url = kwargs.get("scraper_page_url")
        self.scraper_page_id = kwargs.get("scraper_page_id")
        self.client = None
