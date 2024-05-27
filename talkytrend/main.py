"""
 TalkyTrend Main
"""

from datetime import date, datetime

import aiohttp
import finnhub
import requests
import xmltodict
import yfinance as yf
from bs4 import BeautifulSoup
from loguru import logger
from prettytable import PrettyTable
from tradingview_ta import TA_Handler

from talkytrend import __version__
from talkytrend.config import settings


class TalkyTrend:
    """
    TalkyTrend Main Class to interact with market news,
    financial instruments analysis and news and economics
    events.
    """

    def __init__(self):
        """
        Initialize the TalkyTrend class
        """
        self.enabled = settings.talkytrend_enabled
        if not self.enabled:
            return
        self.enable_signals = settings.enable_signals
        self.assets = settings.assets
        self.format = settings.format or None

        self.enable_yfinance = settings.enable_yfinance
        self.yfinance_ticker_reference = settings.yfinance_ticker_reference

        self.enable_events = settings.enable_events
        self.economic_calendar = settings.economic_calendar
        self.fomc_decision_date = settings.fomc_decision_date
        self.live_tv = settings.live_tv_url

        self.enable_feed = settings.enable_feed
        self.feed_url = settings.feed_url

        self.enable_finnhub = settings.enable_finnhub
        self.finnhub_api_key = settings.finnhub_api_key
        self.finnhub_news_category = settings.finnhub_news_category

        self.enable_scraper = settings.enable_scraper
        self.scraper_page_url = settings.scraper_page_url
        self.scraper_page_id = settings.scraper_page_id

    async def get_talkytrend_info(self):
        """
        Get information about the TalkyTrend version.

        :return: A string containing the TalkyTrend version.
        """
        _info = f"ℹ️ {type(self).__name__} {__version__}\n"
        _info += f"signals enabled: {self.enable_signals}\n"
        _info += f"yfinance enabled: {self.enable_yfinance}\n"
        _info += f"events enabled: {self.enable_events}\n"
        _info += f"feed enabled: {self.enable_feed}\n"
        _info += f"scraper enabled: {self.enable_scraper}\n"

        return _info

    async def fetch_analysis(self, asset_id, exchange, screener, interval):
        """
        Fetches from Trading View the analysis
        of a given asset from a specified exchange
        and screener at a specified interval.
        more info:
        https://github.com/AnalyzerREST/python-tradingview-ta

        Args:
            asset_id (str): The ID of the asset.
            exchange (str): The exchange on which
            the asset is traded.
            screener (str): The screener used
            for analysis.
            interval (str): The interval at which
            the analysis is performed.

        Returns:
            str: The recommendation based on the analysis.
            Can be one of the following:
                - 'BUY': "🔼"
                - 'STRONG_BUY': "⏫"
                - 'SELL': "🔽"
                - 'STRONG_SELL': "⏬"
                - Any other value: "▶️"
        """
        try:
            logger.debug(
                "Fetching analysis for {} at {} with screener {} and interval {}.",
                asset_id,
                exchange,
                screener,
                interval,
            )
            handler = TA_Handler(
                symbol=asset_id, exchange=exchange, screener=screener, interval=interval
            )
            analysis = handler.get_analysis()
            if analysis.summary["RECOMMENDATION"] == "BUY":
                return "🔼"
            elif analysis.summary["RECOMMENDATION"] == "STRONG_BUY":
                return "⏫"
            elif analysis.summary["RECOMMENDATION"] == "SELL":
                return "🔽"
            elif analysis.summary["RECOMMENDATION"] == "STRONG_SELL":
                return "⏬"
            else:
                return "▶️"
        except Exception as error:
            logger.warning("event {}", error)

    async def fetch_signal(self, interval="4h"):
        """
        Fetches the signal for a given interval.

        Args:
            interval (str): The interval for which
            to fetch the signal. Defaults to "4h".

        Returns:
            str: The signal table as a string or HTML formatted
        """
        signals = []
        table = PrettyTable(header=False)
        logger.debug("Fetching signal for interval {}", interval)

        for asset in self.assets:
            current_signal = await self.fetch_analysis(
                asset_id=asset["id"],
                exchange=asset["exchange"],
                screener=asset["screener"],
                interval=interval,
            )
            if current_signal:
                signal_item = {
                    "symbol": asset["id"],
                    "interval": interval,
                    "signal": current_signal,
                }
                table.add_row([asset["id"], current_signal])
                signals.append(signal_item)
        return table.get_html_string() if self.format == "HTML" else table.get_string()

    async def fetch_ticker_info(self, ticker=None):
        """
        Fetches the information for a given instrument from
        yahoo finance.

        Args:
            ticker_reference (str): The ticker symbol or
            reference of the instrument. Defaults to "MSFT".

        Returns:
            str: The formatted string containing the title
            and link of the latest news article for the instrument.
                 Returns None if there is no news available.
        """
        if not ticker:
            ticker = self.yfinance_ticker_reference
        logger.debug("Fetching news for {}", ticker)
        ticker = yf.Ticker(ticker)
        if news := ticker.news:
            title = news[0].get("title")
            link = news[0].get("link")
            return f"🗞️ <a href='{link}'>{title}</a>"

    async def fetch_event(self):
        """
        Retrieves the next high-impact economic event
        from the economic calendar.

        :return: A formatted string representing the next high-impact
        economic event, or None if no such event is found.
        """

        def filter_events(data, today):
            """
            Filters a list of events based on their date.

            Args:
                data (list): A list of dictionaries representing events.
                today (str): The date to compare the event dates against.

            Returns:
                list: A list of events with a date greater than today.
            """
            return [event for event in data if event.get("date", "") > today]

        def is_usd_high_impact(event):
            """
            Check if the given event is a high-impact event for the USD or ALL currency.

            Parameters:
                event (dict): The event to check.

            Returns:
                bool: True if the event is a high-impact event
                for the USD or ALL currency and False otherwise.
            """
            return event.get("impact") in {
                "High",
                "Holiday",
            } and event.get("country") in {
                "USD",
                "ALL",
            }

        def is_all_high_impact(event):
            """
            Check if the given event is a high-impact event for the "ALL" country.

            Args:
                event (dict): The event to check.

            Returns:
                bool: True if the event has a "High" or "Holiday" impact
                and is for the "ALL" country, False otherwise.
            """
            return (
                event.get("impact")
                in {
                    "High",
                    "Holiday",
                }
                and event.get("country") == "ALL"
            )

        def is_opec_or_fomc(event):
            """
            Check if the given event is related to OPEC
            (Organization of the Petroleum Exporting Countries)
            or FOMC (Federal Open Market Committee).

            Parameters:
                event (dict): The event to check.

            Returns:
                bool: True if the event is related to OPEC or FOMC, False otherwise.
            """
            return "OPEC" in event.get("title") or "FOMC" in event.get("title")

        def format_event(event):
            """
            Formats an event into a string representation.

            Args:
                event (dict): A dictionary representing
                an event with 'title' and 'date' keys.

            Returns:
                str: A formatted string representing the event,
                with the title and date separated by a newline character.
            """
            return f"💬 {event['title']}\n⏰ {event['date']}"

        async with aiohttp.ClientSession() as session:
            async with session.get(self.economic_calendar, timeout=10) as response:
                logger.debug("Fetching events from {}", self.economic_calendar)
                response.raise_for_status()
                data = await response.json()
                today = datetime.now().isoformat()
                events = filter_events(data, today)
                for event in events:
                    if is_usd_high_impact(event) or is_all_high_impact(event):
                        return format_event(event)
                    if is_opec_or_fomc(event):
                        return format_event(event)

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

    async def check_fomc(self):
        """
        Check if there is an FOMC (Federal Open Market Committee)
        decision on the current date. settings.fomc_decision_date
        is taking a list of dates.

        This function takes no parameters.

        Returns:
            bool: True if there is an FOMC decision
            on the current date, False otherwise.
        """
        logger.debug("Checking for FOMC decision")
        event_dates = self.fomc_decision_date
        current_date = date.today().isoformat()
        return any(event.startswith(current_date) for event in event_dates)

    async def get_tv(self):
        """
        Asynchronously retrieves the URL for TV feed.

        Returns:
            str: An URL representing the live TV
            url if available, otherwise None.
        """
        if self.live_tv:
            return f"📺: {self.live_tv}"

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """
        results = []
        logger.debug("Monitoring")
        if self.enable_events:
            if event := await self.fetch_event():
                results.append(event)

        if self.enable_feed:
            if feed := await self.fetch_feed():
                results.append(feed)

        if self.enable_yfinance:
            if ticker_info := await self.fetch_ticker_info(
                ticker=self.yfinance_ticker_reference
            ):
                results.append(ticker_info)

        if self.enable_signals:
            if signal := await self.fetch_signal():
                results.append(signal)

        if self.enable_scraper:
            if news := await self.scrape_page():
                results.append(news)

        return "\n".join(results)

    async def get_finnhub_news(self):
        """
        Asynchronously retrieves news articles from the Finnhub API
        based on the specified category and API key.

        :return: A string containing HTML formatted news summaries
        linked to their respective URLs.
        Returns None if an error occurs while retrieving the news.
        """
        try:
            finnhub_client = finnhub.Client(api_key=self.finnhub_api_key)
            news_data = finnhub_client.general_news(
                self.finnhub_news_category, min_id=0
            )
            # Create HTML formatted string for each news item
            news_summary_html = (
                f"<a href='{item['url']}' target='_blank'>{item['headline']}</a>"
                f"<br/><p>{item['summary']}</p>"
                for item in news_data
                if "headline" in item and "url" in item and "summary" in item
            )

            return "<br/>".join(news_summary_html)
        except Exception as e:
            logger.error("Error getting finnhub news: {}", e)

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
