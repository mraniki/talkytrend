# from ._client import Client


# class WebsocketHandler(Client):
#     """
#     Websocket client

#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """

#         super().__init__(**kwargs)
#         if self.enabled:
#             self.client = "websocket"
#             self.websocket_url = "wss://echo.websocket.org/"
