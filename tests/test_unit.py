"""
talkytrend Unit Testing
"""

import pytest
from unittest.mock import patch, Mock
from talkytrend import TalkyTrend, TalkyBreaking

@pytest.fixture
def trend():
    """return TrendPlugin"""
    return TalkyTrend()

@pytest.fixture
def breaking():
    """return TrendPlugin"""
    return TalkyBreaking()


@pytest.mark.asyncio
async def test_fetch_analysis(trend):
    print(trend)
    result = await trend.fetch_analysis()
    print(result)
    assert result is not None


@pytest.mark.asyncio
async def test_fetch_analysis_crypto():
    crypto_trend = TalkyTrend(
        asset='BTCUSDT',
        exchange='Binance',
        screener='crypto',
        interval='Interval.INTERVAL_15_MINUTES')
    print(crypto_trend)
    result = await crypto_trend.fetch_analysis()
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_fetch_key_events(breaking):
    print(breaking)
    result = await breaking.key_events()
    print(result)
    assert result is not None