"""
talkytrend Unit Testing
"""

import pytest

from talkytrend import TalkyTrend
from talkytrend.config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(name="talky")
def talky_fixture():
    return TalkyTrend()


@pytest.mark.asyncio
async def test_talkytrend(talky):
    assert isinstance(talky, TalkyTrend)
    assert talky.clients is not None
    assert callable(talky.get_info)
    assert callable(talky.monitor)
    assert callable(talky.fetch_signal)
    assert callable(talky.fetch_feed)
    assert callable(talky.fetch_page)
    assert callable(talky.fetch_tv)
    assert settings.VALUE == "On Testing"
    for cli in talky.clients:
        assert cli is not None
        assert callable(cli.fetch)
        assert callable(cli.monitor)


@pytest.mark.asyncio
async def test_get_info(talky):
    result = await talky.get_info()
    print(result)
    assert result is not None
    assert "TalkyTrend" in result
    assert "ℹ️" in result


@pytest.mark.asyncio
async def test_monitor(talky):
    result = await talky.monitor()
    print(result)
    assert result is not None
    strings = ["EURUSD", "📰", "🗞️", "📺", "💬", "⏰"]
    assert any(string in result for string in strings)


# @pytest.mark.asyncio
# async def test_fetch_signal(talky):
#     print(talky)
#     result = await talky.fetch_signal()
#     print(result)
#     assert result is not None
#     assert "EURUSD" in result


# @pytest.mark.asyncio
# async def test_interval_fetch_signal(talky):
#     print(talky)
#     result = await talky.fetch_signal(interval="1D")
#     print(result)
#     assert result is not None
#     assert "EURUSD" in result


# @pytest.mark.asyncio
# async def test_invalid_interval_fetch_signal(talky):
#     print(talky)
#     result = await talky.fetch_signal(interval="3T")
#     print(result)
#     assert result is not None
#     assert "EURUSD" in result


# @pytest.mark.asyncio
# async def test_fetch_event(talky):
#     result = await talky.fetch_event()
#     assert result is None or isinstance(result, str)


# @pytest.mark.asyncio
# async def test_fetch_feed(talky):
#     result = await talky.fetch_feed()
#     print(result)
#     assert result is not None


# @pytest.mark.asyncio
# async def test_check_fomc(talky):
#     result = await talky.check_fomc()
#     print(result)
#     assert result is not None
#     assert result is False


# @pytest.mark.asyncio
# async def test_fetch_ticker_info(talky):
#     result = await talky.fetch_ticker_info()
#     print(result)
#     assert result is not None
#     assert "yahoo" in result


# @pytest.mark.asyncio
# async def test_get_tv(talky):
#     result = await talky.get_tv()
#     print(result)
#     assert result is not None


# @pytest.mark.asyncio
# async def test_monitor(talky):
#     result = await talky.monitor()
#     print(result)
#     assert result is not None
#     # assert "💬" in result
#     assert "📰" in result
#     assert "EURUSD" in result
#     assert "yahoo" in result


# @pytest.mark.asyncio
# async def test_get_finnhub_news(talky):
#     result = await talky.get_finnhub_news()
#     assert result is not None


# @pytest.mark.asyncio
# async def test_scrape_page(talky):
#     result = await talky.scrape_page()
#     print(result)
#     assert result is not None
