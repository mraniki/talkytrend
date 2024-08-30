import json
import sys
import threading
import time

import tradingeconomics as te
import websocket
from loguru import logger

from .client import Client


class TradingeconomicsHandler(Client):
    """
    Trading Economics API client

    documentation: https://github.com/tradingeconomics/tradingeconomics-python

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled:
            te.login(userkey=self.api_key)

    async def fetch(self):
        """ """
        data = te.getNews(country=["United States"])
        logger.debug("Data: {}", data)
        return data

    async def stream(self):
        """ """
        logger.debug("Starting the socket.")

        def _on_message(web_sock, message):
            """
            made so we do not have to reinitialize connection
            """
            t = threading.Thread(
                # target=on_message,
                args=(
                    web_sock,
                    message,
                ),
            )
            t.start()
            # on_message(web_sock, message)

        web_sock = websocket.WebSocketApp(
            "ws://stream.tradingeconomics.com/?client="
            + self.api_key
            + ":"
            + self.api_key,
            on_message=_on_message,
            # on_error=on_error,
            # on_close=on_close,
        )

        web_sock.on_open = on_open
        try:
            print("RUN")
            web_sock.run_forever()
        # except KeyboardInterrupt:
        except:
            # print(traceback.print_exc())
            logger.debug("exception on the run_forever()")
            sys.exit("Error. Exiting...")
        logger.debug("End of start_socket()")
        web_sock.close()


def on_open(web_sock):
    """subscribe to calendar
    needs to sleep to subscribe multiple times
    """
    print("Open")
    # web_sock.send(json.dumps({'topic': 'subscribe', 'to': 'calendar'}))
    web_sock.send(json.dumps({"topic": "subscribe", "to": "EURUSD:CUR"}))
    time.sleep(2)


# def on_message(web_sock, message):  # pylint: disable=W0613
#     """
#         on_message  stamps message and inserts into pymongo
#     """
#     print( json.loads(message), str(dt.datetime.utcnow()))

#     json.loads(message)

#     if settle_date() != SETTLE_DATE:
#         logging.debug("settle_date != SETTLE_DATE")
#         sys.exit(0)
