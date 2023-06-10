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
    def __init__(self,
                 asset=None,
                 exchange="FX_IDC",
                 screener="forex",
                 interval=Interval.INTERVAL_4_HOURS):
        self.logger = logging.getLogger(name="TalkyTrend")
        if asset is None:
            asset = settings.asset
        self.enabled = settings.talkytrend_status
        self.asset = asset
        self.exchange = exchange
        self.screener = screener
        self.interval = interval
        self.asset_signals = {'4h': None} 

    async def fetch_analysis(self):
        
        # Initialize the TA_Handler
        handler = TA_Handler(
        symbol=self.asset,
        exchange=self.exchange,
        screener=self.screener,
        interval=self.interval)

        analysis = handler.get_analysis()
        print(analysis)
        return analysis.summary['RECOMMENDATION']

    async def check_signal(self):
        current_signal = await self.fetch_analysis()
        if self.asset_signals[self.interval] and current_signal != self.asset_signals[self.interval]:
            message = f'New signal for {self.asset} ({self.interval}): {current_signal}'
            print(message)
            self.asset_signals[self.interval] = current_signal
            return message
            
    async def monitor_assets(self):
        while True:
            await asyncio.gather(*[self.check_signal()])
            await asyncio.sleep(settings.scanner_frequency)

class TalkyBreaking:
    def __init__(self):
        self.logger = logging.getLogger(name="TalkyBreaking")
        self.economic_calendar = settings.economic_calendar
        self.news_url = f"{settings.news_url}{settings.news_api_key}"

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
            print("Title: ", article['title'])
            print("Description: ", article['description'])

    async def monitor_events(self):
        while True:
            await asyncio.gather(*[self.fetch_key_events()])
            await asyncio.sleep(settings.scanner_frequency)