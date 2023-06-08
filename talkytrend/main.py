"""
 talky trend Main
"""

import asyncio
import logging 

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
        # If there's a previous signal and the current signal is different, print a message
        if self.asset_signals[self.interval] and current_signal != self.asset_signals[self.interval]:
            message = f'New signal for {self.asset} ({self.interval}): {current_signal}'
            print(message)
            self.asset_signals[self.interval] = current_signal
            return message
            
    async def monitor_assets(self):
        while True:
            await asyncio.gather(*[self.check_signal()])
            await asyncio.sleep(settings.scanner_frequency)
