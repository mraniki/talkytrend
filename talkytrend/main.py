"""
 TalkyTrend Main
"""

from datetime import date, datetime

import aiohttp
import xmltodict
import yfinance as yf
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
        self.assets = settings.assets
        self.economic_calendar = settings.economic_calendar
        self.live_tv = settings.live_tv_url

    async def get_talkytrend_info(self):
        """
        Get information about the TalkyTrend version.

        :return: A string containing the TalkyTrend version.
        """
        return f"ℹ️ {type(self).__name__} {__version__}\n"

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
            str: The signal table as a string.
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

        return table.get_string()

    async def fetch_ticker_info(self, ticker=settings.ticker_reference):
        """
        Fetches the information for a given instrument from
        yahoo finance. Not yet implemented.

        Args:
            ticker_reference (str): The ticker symbol or
            reference of the instrument. Defaults to "MSFT".

        Returns:
            str: The formatted string containing the title
            and link of the latest news article for the instrument.
                 Returns None if there is no news available.
        """
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
            return [event for event in data if event.get("date", "") > today]

        def is_usd_high_impact(event):
            return event.get("impact") == "High" and event.get("country") in {
                "USD",
                "ALL",
            }

        def is_all_high_impact(event):
            return event.get("impact") == "High" and event.get("country") == "ALL"

        def is_opec_or_fomc(event):
            return "OPEC" in event.get("title") or "FOMC" in event.get("title")

        def format_event(event):
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
            async with session.get(settings.news_feed, timeout=10) as response:
                logger.debug("Fetching news from {}", settings.news_feed)
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
        event_dates = settings.fomc_decision_date
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
        if settings.enable_events:
            if event := await self.fetch_event():
                results.append(event)

        if feed := await self.fetch_feed():
            if settings.enable_feed:
                results.append(feed)

        if settings.enable_yfinance:
            if ticker_info := await self.fetch_ticker_info():
                results.append(ticker_info)

        if signal := await self.fetch_signal():
            if settings.enable_signals:
                results.append(signal)

        return "\n".join(results)
