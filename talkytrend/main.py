"""
 talky trend Main
"""

import asyncio
from datetime import date, datetime, timezone

import aiohttp
import xmltodict
import yfinance as yf

# import logging
from loguru import logger
from prettytable import PrettyTable
from tradingview_ta import TA_Handler

from talkytrend import __version__
from talkytrend.config import settings


class TalkyTrend:
    def __init__(self):
        self.logger = logger
        # logging.getLogger("TalkyTrend")
        self.enabled = settings.talkytrend_enabled
        if not self.enabled:
            return
        self.assets = settings.assets
        self.economic_calendar = settings.economic_calendar
        self.live_tv = settings.live_tv_url
        self.commands = settings.talkytrend_commands

    async def get_talkytrend_info(self):
        return (f"ℹ️ TalkyTrend v{__version__}\n")


    async def get_talkytrend_help(self):
        return (f"{self.commands}\n")

    async def fetch_analysis(
        self,
        asset_id,
        exchange,
        screener,
        interval):
        try:
            handler = TA_Handler(
                symbol=asset_id,
                exchange=exchange,
                screener=screener,
                interval=interval
            )
            analysis = handler.get_analysis()
            # return analysis.summary["RECOMMENDATION"] as str
            if analysis.summary["RECOMMENDATION"] == 'BUY':
                return "🔼"
            elif analysis.summary["RECOMMENDATION"] == 'STRONG_BUY':
                return "⏫"
            elif analysis.summary["RECOMMENDATION"] == 'SELL':
                return "🔽"
            elif analysis.summary["RECOMMENDATION"] == 'STRONG_SELL':
                return "⏬"
            else:
                return "▶️"
        except Exception as error:
            self.logger.warning("event {}", error)

    async def fetch_signal(self, interval="4h"):
        signals = []
        table = PrettyTable()
        table.field_names = [" Trend ", interval]

        for asset in self.assets:
            current_signal = await self.fetch_analysis(
                asset_id=asset["id"],
                exchange=asset["exchange"],
                screener=asset["screener"],
                interval=interval
            )
            if current_signal:
                signal_item = {
                    "symbol": asset["id"],
                    "interval": interval,
                    "signal": current_signal
                }
                table.add_row([asset["id"], current_signal])
                signals.append(signal_item)

        return table.get_string()

    async def fetch_instrument_info(self, ticker_reference="MSFT"):
        ticker = yf.Ticker(ticker_reference)
        if news := ticker.news:
            title = news[0].get("title")
            link = news[0].get("link")
            return f"{title} - {link}"

    async def fetch_event(self):
        def filter_events(data, today):
            return [event for event in data if event.get('date', '') > today]

        def is_usd_high_impact(event):
            return (
                event.get('impact') == 'High' and
                event.get('country') in {'USD', 'ALL'}
            )

        def is_all_high_impact(event):
            return event.get('impact') == 'High' and event.get('country') == 'ALL'

        def is_opec_or_fomc(event):
            return "OPEC" in event.get('title') or "FOMC" in event.get('title')

        def format_event(event):
            return f"💬 {event['title']}\n⏰ {event['date']}"

        async with aiohttp.ClientSession() as session:
            async with session.get(self.economic_calendar, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                today = datetime.now().isoformat()
                events = filter_events(data, today)
                for event in events:
                    if is_usd_high_impact(event) or is_all_high_impact(event):
                        return format_event(event)
                    if is_opec_or_fomc(event):
                        return format_event(event)
        return None
 
    async def fetch_feed(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(settings.news_feed, timeout=10) as response:
                    data = (
                        xmltodict.parse(await response.text())
                        .get('rss')
                        .get('channel')['item'][0]
                    )
                    title = data['title']
                    link = data['link']
                    return f"📰 <a href='{link}'>{title}</a>"
        except Exception as error:
            self.logger.warning("feed {}", error)
            return None

    async def check_fomc(self):
        event_dates = settings.fomc_decision_date
        current_date = date.today().isoformat()
        return any(event.startswith(current_date) for event in event_dates)

    async def get_tv(self):
        if self.live_tv:
            return f"📺: {self.live_tv}"

    async def monitor(self):
        results = []

        if settings.enable_events:
            if event := await self.fetch_event():
                results.append(event)

        if feed := await self.fetch_feed():
            if settings.enable_feed:
                results.append(feed)

        if signal := await self.fetch_signal():
            if settings.enable_signals:
                results.append(signal)

        return "\n".join(results)