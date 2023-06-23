"""
talkytrend Unit Testing
"""

# from unittest.mock import patch, Mock
import pytest
from talkytrend.main import TalkyTrend
from talkytrend.config import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(name="talky")
def talky_fixture():
    """return TrendPlugin"""
    talky = TalkyTrend()
    return talky


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
async def test_check_fomc(talky):
    result = await talky.check_fomc()
    print(result)
    assert result is not None
 

