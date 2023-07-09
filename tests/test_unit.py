"""
talkytrend Unit Testing
"""

from unittest.mock import MagicMock
import pytest
from talkytrend.main import TalkyTrend
from talkytrend.config import settings


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
async def test_check_signal(talky):
    print(talky)
    result = await talky.check_signal()
    print(result)
    assert result is not None


@pytest.mark.asyncio
async def test_fetch_key_events(talky):
    result = await talky.fetch_key_events()
    assert result is None or isinstance(result, str)

#@pytest.mark.asyncio
#async def test_fetch_key_news(talky):
#    result = await talky.fetch_key_news()
#    print(result)
#    assert result is not None

@pytest.mark.asyncio
async def test_fetch_key_feed(talky):
   result = await talky.fetch_key_feed()
   print(result)
   assert result is not None


@pytest.mark.asyncio
async def test_check_fomc(talky):
    result = await talky.check_fomc()
    print(result)
    assert result is not None
 

@pytest.mark.asyncio
async def test_scanner(talky):
    talky.fetch_key_events = MagicMock(return_value='Mocked key events')
    talky.fetch_key_news = MagicMock(return_value='Mocked key news')
    talky.fetch_key_feed = MagicMock(return_value='Mocked key feed')
    talky.check_signal = MagicMock(return_value='Mocked signals')
    async for result in talky.scanner():
        assert result is not None
