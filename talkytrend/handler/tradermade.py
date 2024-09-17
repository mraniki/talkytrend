# import tradermade as tm
# from loguru import logger

# from ._client import Client


# class TradermadeHandler(Client):
#     """
#     Tradermade API client
#     documentation: https://github.com/tradermade/Python-SDK
#     or https://tradermade.com/tutorials/python-sdk-for-forex-data


#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """

#         super().__init__(**kwargs)
#         if self.enabled:
#             self.client = "tradermade"
#             logger.info("Initializing Tradermade")
#             tm.set_rest_api_key(self.api_key)

#     async def get_news(self):
#         """ """
#         # TODO
#         # return tm.live(currency="EURUSD,GBPUSD", fields=["bid", "mid", "ask"])
#         data = tm.live(currency="EURUSD,GBPUSD", fields=["bid", "mid", "ask"])

#         try:
#             # Convert the data to a string format
#             result = []
#             for currency, values in data.items():
#                 result.append(f"{currency}:")
#                 result.extend(
# f"  {field}: {value}" for field, value in values.items())
#             return "\n".join(result)
#         except Exception as e:
#             return f"Error fetching currency data: {str(e)}"
