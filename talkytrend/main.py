"""
 talky trend Main
"""
__version__ = "0.0.0"

import logging 
from .config import settings


import asyncio
from tradingview_ta import TA_Handler, Interval


class TrendPlugin:
    def __init__(self, assets=None):
        if assets is None:
            assets = settings.assets  # Use the default assets if none are provided

        self.assets = assets
        # Initialize a dictionary to store asset signals
        self.asset_signals = {asset: {'15m': None, '4h': None} for asset in self.assets}

    async def fetch_analysis(self, asset, interval):
        # Initialize the TA_Handler for the asset
        handler = TA_Handler()
        handler.set_symbol_as(asset)
        handler.set_screener_as("forex")

        if interval == '15m':
            handler.set_interval_as(Interval.INTERVAL_15_MINUTES)
        elif interval == '4h':
            handler.set_interval_as(Interval.INTERVAL_4_HOURS)

        # Fetch the technical analysis summary
        analysis = handler.get_analysis()

        return analysis.summary['RECOMMENDATION']

    async def check_signal(self, asset):
        for interval in ['15m', '4h']:
            current_signal = await self.fetch_analysis(asset, interval)

            # If there's a previous signal and the current signal is different, print a message
            if self.asset_signals[asset][interval] and current_signal != self.asset_signals[asset][interval]:
                print(f'New signal for {asset} ({interval}): {current_signal}')

            # Store the current signal
            self.asset_signals[asset][interval] = current_signal

    async def monitor_assets(self):
        while True:
            await asyncio.gather(*[self.check_signal(asset) for asset in self.assets])
            await asyncio.sleep(600)

