"""
talkytrend Unit Testing
"""

import pytest
import asyncio
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
    async def stop_scanning():
        stop_scanning_result = await talky.allow_scanning(enable=False)
        assert stop_scanning_result is False

    scanner_task = asyncio.create_task(talky.scanner())
    stop_task = asyncio.create_task(stop_scanning())

    while True:
        done, _ = await asyncio.wait([scanner_task, stop_task], return_when=asyncio.FIRST_COMPLETED)

        if scanner_task in done:
            message = scanner_task.result()
            print("scanner:\n", message)
            assert message is not None
            assert ("📰" in message or "💬" in message or "BTCUSD" in message or "<" in message)
            break

        if stop_task in done:
            break

    scanner_task.cancel()
    stop_task.cancel()