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

    async def fetch_key_events(self):
        calendar = requests.get(self.economic_calendar , timeout=10)
        if calendar.status_code == 200:
            event_list = calendar.json()
            print(event_list)
            for keyval in event_list:
                if (keyval['impact'] == 'High' and keyval['country'] == 'USD'):
                    return keyval

    async def fetch_key_news(self):
        return

    async def monitor_events(self):
        while True:
            await asyncio.gather(*[self.fetch_key_events()])
            await asyncio.sleep(settings.scanner_frequency)