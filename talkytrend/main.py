"""
 talky trend Main
"""

import asyncio
import logging
from datetime import date
import aiohttp
from prettytable import PrettyTable, MARKDOWN
from tradingview_ta import TA_Handler
from talkytrend import __version__
from talkytrend.config import settings

class TalkyTrend:
    def __init__(self):
        try:
            self.logger = logging.getLogger("TalkyTrend")
            self.enabled = settings.talkytrend_enabled
            if not self.enabled:
                return
            self.mode = settings.talkytrend_mode
            self.assets = settings.assets
            self.asset_signals = {}
            self.economic_calendar = settings.economic_calendar
            self.news_url = f"{settings.news_url}{settings.news_api_key}" if settings.news_api_key else None
            self.live_tv = settings.live_tv_url
        except Exception as error:
            self.logger.error("TalkyTrend init error %s",error)

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
            return analysis.summary["RECOMMENDATION"]
        except Exception as error:
            self.logger.error("event %s",error)

    async def check_signal(self):
        try:
            signals = []
            table = PrettyTable()
            table.field_names = ["Asset", "4h"]
            for asset in self.assets:
                current_signal = await self.fetch_analysis(
                    asset_id=asset["id"],
                    exchange=asset["exchange"],
                    screener=asset["screener"],
                    interval=asset["interval"]
                )
                if self.is_new_signal(asset["id"], asset["interval"], current_signal):
                    signal_item = {
                        "symbol": asset["id"],
                        "interval": asset["interval"],
                        "signal": current_signal
                    }
                    self.update_signal(asset["id"], asset["interval"], current_signal)
                    table.add_row([asset["id"], current_signal])
                    signals.append(signal_item)
            #return signals
            #return str(table)
            # table.border = False
            table.set_style(MARKDOWN)

            return table.get_string()
        except Exception as error:
            self.logger.error("check_signal %s", error)
            return []



    def is_new_signal(self, asset_id, interval, current_signal):
        if self.asset_signals.get(asset_id):
            if self.asset_signals[asset_id].get(interval) and current_signal != self.asset_signals[asset_id][interval]:
                self.asset_signals[asset_id][interval] = current_signal
                return True
        else:
            self.asset_signals[asset_id] = {interval: current_signal}
            return True
        return False

    def update_signal(self, asset_id, interval, current_signal):
        self.asset_signals[asset_id][interval] = current_signal


    def get_asset_signals(self):
        return self.asset_signals

    async def fetch_key_events(self):
        def filter_events(data, today):
            return [event for event in data if event.get('date', '').startswith(today)]

        def is_usd_high_impact(event):
            return event.get('impact') == 'High' and event.get('country') in {'USD', 'ALL'}

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
                today = date.today().isoformat()
                events = filter_events(data, today)
                for event in events:
                    if is_usd_high_impact(event) or is_all_high_impact(event):
                        return format_event(event)
                    if is_opec_or_fomc(event):
                        return format_event(event)
        return None


    
    async def fetch_key_news(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.news_url, timeout=10) as response:
                    data = await response.json()
                    articles = data.get('articles', [])
                    key_news = [{'title': article['title'], 'url': article['url']} for article in articles]
                    last_item = key_news[-1]
                    return f"{last_item['title']} {last_item['url']}"
        except aiohttp.ClientError as error:
            self.logger.error("news %s", error)
            return None

    async def check_fomc(self):
        event_dates = settings.fomc_decision_date
        current_date = date.today().isoformat()
        return any(event.startswith(current_date) for event in event_dates)


    async def scanner(self):
        while True:
            try:
                if settings.enable_events:
                    key_events = await self.fetch_key_events()
                    if key_events is not None:
                        self.logger.debug("Key event\n%s", key_events)
                        yield key_events
                if settings.enable_news:
                    key_news = await self.fetch_key_news()
                    if key_news is not None:
                        self.logger.debug("Key news\n%s", key_news)
                        yield key_news

                if settings.enable_signals:
                    signals = await self.check_signal()
                    if signals is not None:
                        self.logger.debug("Signals\n%s", signals)
                        yield signals

            except Exception as error:
                self.logger.error("scanner %s", error)

            await asyncio.sleep(settings.scanner_frequency)


