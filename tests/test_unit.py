"""
talkytrend Unit Testing
"""

import pytest
from unittest.mock import patch, Mock
from tradingview_ta import TA_Handler, Interval
from talkytrend import TrendPlugin

@pytest.fixture
def trend():
    """return TrendPlugin"""
    return TrendPlugin()


@pytest.mark.asyncio
async def test_fetch_analysis():
    plugin = TrendPlugin()
    print(plugin)
    result = await plugin.fetch_analysis()
    print(result)
    assert result is not None
 

@pytest.mark.asyncio
async def test_fetch_analysis_crypto():
    plugin = TrendPlugin(asset='BTCUSDT',exchange='Binance',screener='crypto',interval=Interval.INTERVAL_15_MINUTES)
    print(plugin)
    result = await plugin.fetch_analysis()
    print(result)
    assert result is not None
