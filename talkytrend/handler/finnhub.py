# import finnhub
# from loguru import logger

# from .client import Client


# class FinnhubHandler(Client):
#     """
#     Finnhub API client


#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """

#         super().__init__(**kwargs)
#         if self.enabled:
#             self.client = "Finnhub"

#     async def fetch(self):
#         """
#         Asynchronously retrieves news articles from the Finnhub API
#         based on the specified category and API key.

#         :return: A string containing HTML formatted news summaries
#         linked to their respective URLs.
#         Returns None if an error occurs while retrieving the news.
#         """
#         try:
#             finnhub_client = finnhub.Client(api_key=self.api_key)
#             news_data = finnhub_client.general_news(
#                 self.api_category, min_id=0
#             )
#             # Create HTML formatted string for each news item
#             news_summary_html = (
#                 f"<a href='{item['url']}' target='_blank'>{item['headline']}</a>"
#                 f"<br/><p>{item['summary']}</p>"
#                 for item in news_data
#                 if "headline" in item and "url" in item and "summary" in item
#             )

#             return "<br/>".join(news_summary_html)
#         except Exception as e:
#             logger.error("Error getting finnhub news: {}", e)
