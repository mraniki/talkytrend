"""
 talky trend Main
"""
__version__ = "0.0.0"

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
        self.enabled = settings.plugin_trend
        self.asset = asset
        self.exchange = exchange
        self.screener = screener
        self.interval = interval
#         self.asset_signals = {asset: {'15m': None, '4h': None} for asset in self.assets}

    async def fetch_analysis(self):
        # Initialize the TA_Handler 
        handler = TA_Handler(
        symbol=self.asset,
        exchange=self.exchange,
        screener=self.screener,
        interval=self.interval)

        # Fetch the technical analysis summary
        analysis = handler.get_analysis()
        print(analysis)
        return analysis.summary['RECOMMENDATION']

#     async def check_signal(self, asset):
#         for interval in ['15m', '4h']:
#             current_signal = await self.fetch_analysis(asset, interval)

#             # If there's a previous signal and the current signal is different, print a message
#             if self.asset_signals[asset][interval] and current_signal != self.asset_signals[asset][interval]:
#                 print(f'New signal for {asset} ({interval}): {current_signal}')

#             # Store the current signal
#             self.asset_signals[asset][interval] = current_signal

    # async def monitor_assets(self):
    #     while True:
    #         await asyncio.gather(*[self.check_signal(asset) for asset in self.assets])
    #         await asyncio.sleep(600)

