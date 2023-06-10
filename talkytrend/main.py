"""
 talky trend Main
"""

import asyncio
import logging
import requests

from tradingview_ta import TA_Handler, Interval

from talkytrend import __version__
from .config import settings

class TalkyTrend:
    def __init__(self):
        self.economic_calendar = settings.economic_calendar
        self.news_url = f"{settings.news_url}{settings.news_api_key}" if settings.news_api_key else None
        self.enabled = settings.talkytrend_status
        self.assets = settings.assets
        self.asset_signals = {"15m": None, "1h": None, "4h": None}

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
        except Exception as e:
            print(e)


    async def check_signal(self):
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



    def get_asset_signals(self):
        return self.asset_signals

    async def fetch_key_events(self):
        response = requests.get(self.economic_calendar, timeout=10)  
        if response.status_code == 200:
            event_list = response.json()
            for event in event_list:
                impact = event.get('impact')
                country = event.get('country')
                title = event.get('title')
                if impact == 'High' and country in {'USD', 'ALL'}:
                    return event
                if "OPEC" in title or "FOMC" in title:
                    return event

    async def fetch_key_news(self):
        response = requests.get(self.news_url,timeout=10)
        data = response.json()
        articles = data['articles']
        for article in articles:
            # print("Title: ", article['title'])
            # print("Description: ", article['description'])
            return article

    async def scanner(self):
        while True:
            tasks = [self.check_signal()]
            tasks.append(self.fetch_key_events())
            tasks.append(self.fetch_key_news())
            results = await asyncio.gather(*tasks)
            if results[1] is not None:
                print("Key event:", results[1])
            if results[2] is not None:
                print("Key news:", results[2]["title"])
            await asyncio.sleep(settings.scanner_frequency)