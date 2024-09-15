# from loguru import logger
# from polygon import RESTClient

# from ._client import Client


# class PolygonHandler(Client):
#     """
#     Polygon.io client
#     docs: https://github.com/polygon-io/client-python


#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """

#         super().__init__(**kwargs)
#         if self.enabled:
#             self.client = RESTClient(api_key=self.api_key)
#             logger.info("Initializing Polygon.io")

#     async def get_news(self):
#         """ """
#         return self.client.list_ticker_news(self.ticker, order="desc", limit=1)
