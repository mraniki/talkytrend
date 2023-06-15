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

            table_text = table.get_string()
            return table_text
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.economic_calendar, timeout=10) as response:
                    if response.status == 200:
                        event_list = await response.json()
                        today = date.today().isoformat()
                        for event in event_list:
                            impact = event.get('impact')
                            country = event.get('country')
                            title = event.get('title')
                            event_date = event.get('date')
                            if event_date and event_date.startswith(today):
                                if impact == 'High' and country in {'USD', 'ALL'}:
                                    return f"💬 {title}\n⏰ {event_date}"
                                if "OPEC" in title or "FOMC" in title:
                                    return f"💬 {title}\n⏰ {event_date}"
            return None
        except Exception as error:
            self.logger.error("event %s",error)
    
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


