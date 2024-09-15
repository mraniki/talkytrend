from ._client import Client


class LivetvHandler(Client):
    """
    Class for handling live TV.


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "LiveTV"

    async def fetch(self):
        """
        Asynchronously retrieves the URL for TV feed.

        Returns:
            str: An URL representing the live TV
            url if available, otherwise None.
        """
        if self.enabled and self.url:
            return f"📺: {self.url}"

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
