"""
 TalkyTrend Main
"""

import importlib

from loguru import logger

from talkytrend import __version__
from talkytrend.config import settings


class TalkyTrend:
    """
    TalkyTrend Main Class to interact with market news,
    financial instruments analysis and news and economics
    events.
    """

    def __init__(self):
        """
        Initialize the TalkyTrend class
        """
        self.enabled = settings.talkytrend_enabled
        if not self.enabled:
            return

        # Create a mapping of library names to client classes
        self.client_classes = self.get_all_client_classes()
        # logger.debug("client_classes available {}", self.client_classes)

        if not self.enabled:
            logger.info("Module is disabled. No Client will be created.")
            return
        self.clients = []

        # Create a client for each client in settings.myllm
        for name, client_config in settings.talkytrend.items():
            if (
                # Skip empty client configs
                client_config is None
                # Skip non-dict client configs
                or not isinstance(client_config, dict)
                # Skip template and empty string client names
                or name in ["", "template"]
                # Skip disabled clients
                or not client_config.get("enabled")
            ):
                continue
                # Create the client
            logger.debug("Creating client {}", name)
            client = self._create_client(**client_config, name=name)
            # If the client has a valid client attribute, append it to the list
            if client and getattr(client, "client", None):
                self.clients.append(client)

        # Log the number of clients that were created
        logger.info(f"Loaded {len(self.clients)} clients")
        if not self.clients:
            logger.warning(
                "No Client were created. Check your settings or disable the module."
            )

    def _create_client(self, **kwargs):
        """
        Create a client based on the given protocol.

        This function takes in a dictionary of keyword arguments, `kwargs`,
        containing the necessary information to create a client. The required
        key in `kwargs` is "library", which specifies the protocol to use for
        communication with the LLM. The value of "library" must match one of the
        libraries supported by MyLLM.

        This function retrieves the class used to create the client based on the
        value of "library" from the mapping of library names to client classes
        stored in `self.client_classes`. If the value of "library" does not
        match any of the libraries supported, the function logs an error message
        and returns None.

        If the class used to create the client is found, the function creates a
        new instance of the class using the keyword arguments in `kwargs` and
        returns it.

        The function returns a client object based on the specified protocol
        or None if the library is not supported.

        Parameters:
            **kwargs (dict): A dictionary of keyword arguments containing the
            necessary information for creating the client. The required key is
            "library".

        Returns:
            A client object based on the specified protocol or None if the
            library is not supported.

        """
        library = (
            kwargs.get("library")
            or kwargs.get("platform")
            or kwargs.get("protocol")
            or kwargs.get("parser_library")
            or kwargs.get("llm_library")
            or "g4f"
        )
        cls = self.client_classes.get((f"{library.capitalize()}Handler"))
        return None if cls is None else cls(**kwargs)

    def get_all_client_classes(self):
        """
        Retrieves all client classes from the `myllm.provider` module.

        This function imports the `myllm.provider` module and retrieves
        all the classes defined in it.

        The function returns a dictionary where the keys are the
        names of the classes and the values are the corresponding
        class objects.

        Returns:
            dict: A dictionary containing all the client classes
            from the `myllm.provider` module.
        """
        provider_module = importlib.import_module("talkytrend.handler")
        return {
            name: cls
            for name, cls in provider_module.__dict__.items()
            if isinstance(cls, type)
        }

    async def get_talkytrend_info(self):
        """
        Get information about the TalkyTrend version.

        :return: A string containing the TalkyTrend version.
        """
        _info = f"ℹ️ {type(self).__name__} {__version__}\n"
        _info += f"signals enabled: {self.enable_signals}\n"
        _info += f"yfinance enabled: {self.enable_yfinance}\n"
        _info += f"events enabled: {self.enable_events}\n"
        _info += f"feed enabled: {self.enable_feed}\n"
        _info += f"scraper enabled: {self.enable_scraper}\n"

        return _info

    async def monitor(self):
        """
        Asynchronously monitors the system and retrieves
        various data sources based on the configured settings.
        Cover Events, Feed, and Signal.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """
        results = []
        logger.debug("Monitoring")
        if self.enable_events:
            if event := await self.fetch_event():
                results.append(event)

        if self.enable_feed:
            if feed := await self.fetch_feed():
                results.append(feed)

        if self.enable_yfinance:
            if ticker_info := await self.fetch_ticker_info(
                ticker=self.yfinance_ticker_reference
            ):
                results.append(ticker_info)

        if self.enable_signals:
            if signal := await self.fetch_signal():
                results.append(signal)

        if self.enable_scraper:
            if news := await self.scrape_page():
                results.append(news)

        return "\n".join(results)
