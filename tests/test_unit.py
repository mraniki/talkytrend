"""
talkytrend Unit Testing
"""

import pytest
from unittest.mock import patch, Mock
from tradingview_ta import TA_Handler, Interval
from talkytrend import TrendPlugin

@pytest.fixture
def trend():
    """return fmo"""
    return TrendPlugin()


@pytest.mark.asyncio
async def test_fetch_analysis():
    # Mock the TA_Handler class
    with patch("tradingview_ta.TA_Handler") as mock_handler: 
        # Mock the get_analysis method to return a predefined result
        mock_handler.return_value.get_analysis.return_value = {
            "summary": {"RECOMMENDATION": "BUY"}
        }

        # Initialize the plugin with 'EURUSD'
        plugin = TrendPlugin("EURUSD")

        # Call the fetch_analysis method
        result = await plugin.fetch_analysis()

        # Check that the method called the correct methods on the TA_Handler
        mock_handler.return_value.set_symbol_as.assert_called_with("EURUSD")
        #mock_handler.return_value.set_screener_as.assert_called_with("forex")
        #mock_handler.return_value.set_interval_as.assert_called_with(Interval.INTERVAL_15_MINUTES)
        #mock_handler.return_value.get_analysis.assert_called()

        # Check that the method returned the correct result
        assert result == "BUY"