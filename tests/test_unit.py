"""
talkytrend Unit Testing
"""

import pytest

from talkytrend.config import settings
from talkytrend.main import TalkyTrend


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(name="talky")
def talky_fixture():
    return TalkyTrend()


@pytest.mark.asyncio
async def test_talkytrend(talky):
    assert talky is not None
    assert settings.VALUE == "On Testing"

@pytest.mark.asyncio
async def test_get_talkytrend_info(talky):
    result = await talky.get_talkytrend_info()
    print(result)
    assert result is not None
    assert "ℹ️" in result 
    assert "TalkyTrend" in result

@pytest.mark.asyncio
async def test_fetch_signal(talky):
    print(talky)
    result = await talky.fetch_signal()
    print(result)
    assert result is not None
    assert "EURUSD" in result 

@pytest.mark.asyncio
async def test_interval_fetch_signal(talky):
    print(talky)
    result = await talky.fetch_signal(interval="1D")
    print(result)
    assert result is not None
    assert "EURUSD" in result 

@pytest.mark.asyncio
async def test_invalid_interval_fetch_signal(talky):
    print(talky)
    result = await talky.fetch_signal(interval="3T")
    print(result)
    assert result is not None
    assert "EURUSD" in result 

@pytest.mark.asyncio
async def test_fetch_event(talky):
    result = await talky.fetch_event()
    assert result is None or isinstance(result, str)

@pytest.mark.asyncio
async def test_fetch_feed(talky):
   result = await talky.fetch_feed()
   print(result)
   assert result is not None


@pytest.mark.asyncio
async def test_check_fomc(talky):
    result = await talky.check_fomc()
    print(result)
    assert result is not None
    assert result is False

@pytest.mark.asyncio
async def test_get_tv(talky):
    result = await talky.get_tv()
    print(result)
    assert result is not None

@pytest.mark.asyncio
async def test_monitor(talky):
    result = await talky.monitor()
    print(result)
    assert result is not None
    assert result is False
