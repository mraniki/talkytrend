"""
 TalkyTrend Main
"""

import asyncio
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
        self.settings = settings.talkytrend

        if not self.enabled:
            logger.info("Module is disabled. No Client will be created.")
            return

        self.clients = []
        # Create a mapping of library names to client classes
        self.client_classes = self.get_all_client_classes()
        # logger.debug("client_classes available {}", self.client_classes)
        # Create a client for each client in settings.myllm
        for name, client_config in self.settings.items():
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
        library = kwargs.get("library") or "livetv"
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

    async def get_info(self):
        """
        Get information about the
        TalkyTrend version and clients.

        :return: A string containing the TalkyTrend version.
        """
        version_info = f"ℹ️ {type(self).__name__} {__version__}\n"
        client_info = "".join(f"🤖 {client.name}\n" for client in self.clients)
        return version_info + client_info.strip()

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

        for client in self.clients:
            if client:
                result = await client.monitor()
                if result:
                    results.append(result)
        return "\n".join(results)

    async def fetch_signal(self):
        """
        Asynchronously fetches the signal from Tradingview.

        Returns:
            str: A string containing the concatenated results
             of the retrieved signal.
        """
        results = []
        for client in self.clients:
            if client.client == "Tradingview":
                result = await client.fetch()
                if result:
                    results.append(result)
        return "\n".join(results)

    async def fetch_feed(self):
        """
        Asynchronously retrieves the latest news
        from various sources based on the configured
        settings.

        Returns:
            str: A string containing the concatenated
             results of the retrieved news sources.
        """
        results = []
        for client in self.clients:
            if client.client == "Feed":
                result = await client.fetch()
                if result:
                    results.append(result)
        return "\n".join(results)

    async def fetch_page(self):
        """
        Asynchronously scrapes a webpage and retrieves
        the content specified by the scraper_page_url
        and scraper_page_id attributes.

        :return: The content of the webpage as a string,
        formatted using BeautifulSoup.
        If the scraper_page_id is not specified,
        the entire webpage is returned.

        :rtype: str
        """
        results = []
        for client in self.clients:
            if client.client == "Scraper":
                result = await client.fetch()
                if result:
                    results.append(result)
        return "\n".join(results)

    scrape_page = fetch_page

    async def fetch_tv(self):
        """
        Asynchronously retrieves the URL for TV feed.

        Returns:
            str: An URL representing the live TV
            url if available, otherwise None.
        """
        results = []
        for client in self.clients:
            if client.client == "LiveTV":
                result = await client.fetch()
                if result:
                    results.append(result)
        return "\n".join(results)

    get_tv = fetch_tv

    async def get_news(self):
        """
        Asynchronously retrieves the latest news
        from various sources based on the configured
        settings.

        Returns:
            str: A string containing the concatenated
             results of the retrieved news sources.
        """
        results = []
        for client in self.clients:
            result = await client.get_news()
            logger.debug("Result from {}: {}", client.library, result)
            if result and isinstance(result, str):
                results.append(result)
            else:
                logger.warning("Skipping non-string result from client: {}", result)
        return "\n".join(results)

    async def get_stream(self):
        """
        Asynchronously streams data from the source
        using the configured settings.

        Returns:
            str: A string containing the concatenated results
             of the retrieved data sources.
        """
        results = []
        for client in self.clients:
            if client.stream:
                async for result in client.stream():
                    results.append(result)
        return "\n".join(results)

    async def continuous_stream(self):
        """
        Continuously fetches stream data and handles it.
        """
        while True:
            try:
                result = await self.get_stream()
                logger.info(result)  # or handle the result as needed
            except Exception as e:
                logger.error(f"Error occurred: {e}")
            await asyncio.sleep(1)  # Add a delay if needed to prevent tight loop
