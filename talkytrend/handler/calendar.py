from datetime import datetime

import aiohttp
from loguru import logger

from ._client import Client


class CalendarHandler(Client):
    """

    CalendarHandler to retrieve economic events
    from the forexfactory economic calendar.


    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            self.client = "Calendar"

    async def fetch(self):
        """
        Retrieves the next high-impact economic event
        from the economic calendar.

        :return: A formatted string representing the next high-impact
        economic event, or None if no such event is found.
        """

        def filter_events(data, today):
            """
            Filters a list of events based on their date.

            Args:
                data (list): A list of dictionaries representing events.
                today (str): The date to compare the event dates against.

            Returns:
                list: A list of events with a date greater than today.
            """
            return [event for event in data if event.get("date", "") > today]

        def is_usd_high_impact(event):
            """
            Check if the given event is a high-impact event for the USD or ALL currency.

            Parameters:
                event (dict): The event to check.

            Returns:
                bool: True if the event is a high-impact event
                for the USD or ALL currency and False otherwise.
            """
            return event.get("impact") in {
                "High",
                "Holiday",
            } and event.get("country") in {
                "USD",
                "ALL",
            }

        def is_all_high_impact(event):
            """
            Check if the given event is a high-impact event for the "ALL" country.

            Args:
                event (dict): The event to check.

            Returns:
                bool: True if the event has a "High" or "Holiday" impact
                and is for the "ALL" country, False otherwise.
            """
            return (
                event.get("impact")
                in {
                    "High",
                    "Holiday",
                }
                and event.get("country") == "ALL"
            )

        def is_opec_or_fomc(event):
            """
            Check if the given event is related to OPEC
            (Organization of the Petroleum Exporting Countries)
            or FOMC (Federal Open Market Committee).

            Parameters:
                event (dict): The event to check.

            Returns:
                bool: True if the event is related to OPEC or FOMC, False otherwise.
            """
            return "OPEC" in event.get("title") or "FOMC" in event.get("title")

        def format_event(event):
            """
            Formats an event into a string representation.

            Args:
                event (dict): A dictionary representing
                an event with 'title' and 'date' keys.

            Returns:
                str: A formatted string representing the event,
                with the title and date separated by a newline character.
            """
            return f"💬 {event['title']}\n⏰ {event['date']}"

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, timeout=10) as response:
                logger.debug("Fetching events from {}", self.url)
                response.raise_for_status()
                data = await response.json()
                today = datetime.now().isoformat()
                events = filter_events(data, today)
                for event in events:
                    if is_usd_high_impact(event) or is_all_high_impact(event):
                        return format_event(event)
                    if is_opec_or_fomc(event):
                        return format_event(event)


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
