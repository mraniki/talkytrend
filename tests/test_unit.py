"""
talkytrend Unit Testing
"""

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
    assert "4h" in result
    assert "EURUSD" in result 

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
async def test_get_tv(talky):
    result = await talky.get_tv()
    print(result)
    assert result is not None


@pytest.mark.asyncio
async def test_scanner(talky):
    stop_scanning = False

    async def stop_scanning_fn():
        nonlocal stop_scanning
        stop_scanning = True
        await talky.allow_scanning(enable=False)

    async for message in talky.scanner():
        assert settings.VALUE == "On Testing"
        assert settings.scanner_frequency == 2
        assert message is not None
        assert ("📰" in message 
                or "💬" in message 
                or "BTCUSD" in message 
                or "<" in message)
        await stop_scanning_fn()
        if stop_scanning:
            break
