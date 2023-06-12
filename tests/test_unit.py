"""
talkytrend Unit Testing
"""

# from unittest.mock import patch, Mock
import pytest
from talkytrend import TalkyTrend

@pytest.fixture(name="talky")
def talky_fixture():
    """return TrendPlugin"""
    return TalkyTrend()

@pytest.mark.asyncio
async def test_check_signal(talky):
    print(talky)
    result = await talky.check_signal()
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_fetch_key_events(talky):
    result = await talky.fetch_key_events()
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def fetch_key_news(talky):
    result = await talky.fetch_key_news()
    print(result)
    assert result is not None
 