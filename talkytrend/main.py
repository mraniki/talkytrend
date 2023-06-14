"""
 talky trend Main
"""

import asyncio
import logging
from datetime import date
import aiohttp
from tradingview_ta import TA_Handler
from talkytrend import __version__
from .config import settings

class TalkyTrend:
    def __init__(self):
        self.logger = logging.getLogger("TalkyTrend")
        self.enabled = settings.talkytrend_enabled
        self.assets = settings.assets
        self.asset_signals = {"15m": None, "1h": None, "4h": None}
        self.economic_calendar = settings.economic_calendar
        self.news_url = f"{settings.news_url}{settings.news_api_key}" if settings.news_api_key else None
        self.live_tv = settings.live_tv_url

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
            messages = []
            for asset in self.assets:
                current_signal = await self.fetch_analysis(
                    asset["id"],
                    asset["exchange"],
                    asset["screener"],
                    asset["interval"])
                if self.asset_signals.get(asset["id"]) and self.asset_signals[asset["id"]].get(asset["interval"]) and current_signal != self.asset_signals[asset["id"]][asset["interval"]]:
                    message = f'New signal for {asset["id"]} ({asset["interval"]}): {current_signal}'
                    print(message)
                    self.asset_signals[asset["id"]][asset["interval"]] = current_signal
                    messages.append(message)
                elif not self.asset_signals.get(asset["id"]):
                    self.asset_signals[asset["id"]] = {asset["interval"]: current_signal}
                else:
                    self.asset_signals[asset["id"]][asset["interval"]] = current_signal
            return messages
        except Exception as error:
            self.logger.error("event %s",error)


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
                                    return f"💬 {title}\n⏰ {event_date}T{event.get('time')}"
                                if "OPEC" in title or "FOMC" in title:
                                    return f"💬 {title}\n⏰ {event_date}T{event.get('time')}"
        except Exception as error:
            self.logger.error("event %s",error)
    
    async def fetch_key_news(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.news_url, timeout=10) as response:
                    data = await response.json()
                    if not (articles := data.get('articles')):
                        return None
                    key_news = []
                    for article in articles:
                        news_item = {
                            'title': article['title'],
                            'url': article['url']
                        }
                        key_news.append(news_item)
                    return key_news
        except Exception as error:
            self.logger.error("news %s",error)
#    async def scanner(self):
#        while True:
#            try:
#                tasks = [self.fetch_key_events(), self.fetch_key_news()]
#                results = await asyncio.gather(*tasks)

#                if results[0] is not None:
#                    print("Key event:", results[0])
#                    return results[0]
                
#                if results[1] is not None:
#                    if results[1]:
#                        print("Key news:", results[1][0])
#                        return results[1]

#            except Exception as e:
#                print(f"Error in scanner loop: {e}")
            
#            await asyncio.sleep(settings.scanner_frequency)
    async def scanner(self):
        while True:
            try:
                tasks = [self.fetch_key_events(), self.fetch_key_news()]
                results = await asyncio.gather(*tasks)

                if results[0] is not None:
                    self.logger.debug("Key event %s",results[0])
                    yield results[0]  # Use 'yield' to return the result as an asynchronous iterator

                if results[1] is not None:
                    if results[1]:
                        self.logger.debug("Key news %s",results[1][0])
                        yield results[1]  # Use 'yield' to return the result as an asynchronous iterator

            except Exception as error:
                self.logger.error("scanner %s",error)
                
