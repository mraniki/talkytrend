"""
talkytrend Unit Testing

"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from talkytrend import TalkyTrend
from talkytrend.config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(name="talky")
def talky_fixture():
    return TalkyTrend()


@pytest.fixture(name="calendar")
async def talky_calendar():
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value=[
            {
                "title": "Fed Chair Powell Speaks",
                "country": "USD",
                "date": "2024-07-15T12:00:00-04:00",
                "impact": "High",
                "forecast": "",
                "previous": "",
                "url": "https://www.forexfactory.com/calendar/717-usd-fed-chair-powell-speaks",
            },
            {
                "title": "Bank Holiday",
                "country": "USD",
                "date": "2024-07-14T19:00:00-04:00",
                "impact": "Holiday",
                "forecast": "",
                "previous": "",
                "url": "https://www.forexfactory.com/calendar/393-jpy-bank-holiday",
            },
            {
                "title": "OPEC Monthly Report",
                "country": "ALL",
                "date": "2024-07-15T00:00:00-04:00",
                "impact": "High",
                "forecast": "",
                "previous": "",
                "url": "https://www.forexfactory.com/calendar",
            },
            {
                "title": "CPI m/m",
                "country": "CAD",
                "date": "2024-07-16T08:30:00-04:00",
                "impact": "High",
                "forecast": "0.1%",
                "previous": "0.6%",
                "url": "https://www.forexfactory.com/calendar/80-cad-cpi-mm",
            },
            {
                "title": "Retail Sales m/m",
                "country": "USD",
                "date": "2024-07-16T08:30:00-04:00",
                "impact": "High",
                "forecast": "-0.2%",
                "previous": "0.1%",
                "url": "https://www.forexfactory.com/calendar/102-usd-retail-sales-mm",
            },
        ]
    )
    return mock_response


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
async def test_fetch_signal(talky):
    result = await talky.fetch_signal()
    print(result)
    assert result is not None
    strings = ["EURUSD"]
    assert any(string in result for string in strings)


@pytest.mark.asyncio
async def test_fetch_feed(talky):
    result = await talky.fetch_feed()
    print(result)
    assert result is not None
    strings = ["euro", "📰"]
    assert any(string in result for string in strings)


@pytest.mark.asyncio
async def test_fetch_page(talky):
    result = await talky.fetch_page()
    print(result)
    assert result is not None


@pytest.mark.asyncio
async def test_fetch_tv(talky):
    result = await talky.fetch_tv()
    print(result)
    assert result is not None
    strings = ["📺"]
    assert any(string in result for string in strings)


async def test_get_news(talky):
    result = await talky.get_news()
    print(result)
    assert result is not None
    # strings = ["📺"]
    # assert any(string in result for string in strings)


async def test_get_stream(talky):
    result = await talky.get_stream()
    print(result)
    assert result is not None
    # strings = ["📺"]
    # assert any(string in result for string in strings)


@pytest.mark.asyncio
async def test_monitor(talky):
    result = await talky.monitor()
    print(result)
    assert result is not None
    strings = ["EURUSD", "📰", "🗞️", "📺", "💬", "⏰"]
    assert any(string in result for string in strings)


@pytest.mark.asyncio
async def test_calendar(talky, calendar):
    with patch("aiohttp.ClientSession.get", return_value=calendar):
        for cli in talky.clients:
            if cli == "Calendar":
                result = await talky.monitor()
                print(result)
                assert result is not None
                assert "💬 Fed Chair Powell Speaks\n⏰ 2024-07-15" in result
                assert "💬 Bank Holiday" in result
