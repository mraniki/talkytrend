from loguru import logger
from prettytable import PrettyTable
from tradingview_ta import TA_Handler

from .client import Client


class TradingviewHandler(Client):
    """
    TradingviewHandler


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        logger.debug("Initializing TradingviewHandler")
        if self.enabled:
            self.client = "Tradingview"

    async def fetch_tv_data(self, asset_id, exchange, screener, interval):
        """
        Fetches from Trading View the analysis
        of a given asset from a specified exchange
        and screener at a specified interval.
        more info:
        https://github.com/AnalyzerREST/python-tradingview-ta

        Args:
            asset_id (str): The ID of the asset.
            exchange (str): The exchange on which
            the asset is traded.
            screener (str): The screener used
            for analysis.
            interval (str): The interval at which
            the analysis is performed.

        Returns:
            str: The recommendation based on the analysis.
            Can be one of the following:
                - 'BUY': "🔼"
                - 'STRONG_BUY': "⏫"
                - 'SELL': "🔽"
                - 'STRONG_SELL': "⏬"
                - Any other value: "▶️"
        """
        # try:
        logger.debug(
            "Fetching analysis for {} at {} with screener {} and interval {}.",
            asset_id,
            exchange,
            screener,
            interval,
        )
        handler = TA_Handler(
            symbol=asset_id, exchange=exchange, screener=screener, interval=interval
        )
        analysis = handler.get_analysis()
        if analysis.summary["RECOMMENDATION"] == "BUY":
            return "🔼"
        elif analysis.summary["RECOMMENDATION"] == "STRONG_BUY":
            return "⏫"
        elif analysis.summary["RECOMMENDATION"] == "SELL":
            return "🔽"
        elif analysis.summary["RECOMMENDATION"] == "STRONG_SELL":
            return "⏬"
        else:
            return "▶️"
        # except Exception as error:
        #     logger.warning("event {}", error)

    async def fetch(self, interval="4h"):
        """
        Fetches the signal for a given interval.

        Args:
            interval (str): The interval for which
            to fetch the signal. Defaults to "4h".

        Returns:
            str: The signal table as a string or HTML formatted
        """
        signals = []
        table = PrettyTable(header=False)
        logger.debug("Fetching signal for interval {}", interval)

        for asset in self.instrument:
            current_signal = await self.fetch_tv_data(
                asset_id=asset["id"],
                exchange=asset["exchange"],
                screener=asset["screener"],
                interval=interval,
            )
            if current_signal:
                signal_item = {
                    "symbol": asset["id"],
                    "interval": interval,
                    "signal": current_signal,
                }
                table.add_row([asset["id"], current_signal])
                signals.append(signal_item)
        return table.get_html_string() if self.format == "HTML" else table.get_string()

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """

        return await self.fetch()
