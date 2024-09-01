"""
Provides example for talkytrend
"""

import asyncio

from talkytrend import TalkyTrend


async def main():
    """Main"""

    talky = TalkyTrend()

    # ticker_info = await talky.fetch_ticker_info()
    # print("ticker_info:\n", ticker_info)

    # trend = await talky.fetch_signal()
    # print("trend:\n", trend)
    # # signal:
    # #  +--------+----+
    # # | Asset  | 4h |
    # # +--------+----+
    # # | EURUSD | 🔼 |

    # feed = await talky.fetch_feed()
    # print("feed:\n", feed)
    #  📰 <a href='https://www.zerohedge.com/political/one-third-seattle-residents-may-flee-city-over-crime-costs'>
    # One-Third Of Seattle Residents May Flee City Over Crime, Costs</a>
    # events = await talky.fetch_event()
    # print("events:\n", events)
    # # 💬 Core PPI m/m
    # # ⏰ 2023-06-14T08:30:00-04:00
    # fomc_day = await talky.check_fomc()
    # print("is it FOMC today:\n", fomc_day)
    # # False

    # news_data = await talky.get_finnhub_news()
    # print(news_data)

    # scrape = await talky.scrape_page()
    # print(scrape)

    # monitor = await talky.monitor()
    # print("monitor:\n", monitor)
    # await talky.get_news()

    await talky.continuous_stream()


if __name__ == "__main__":
    asyncio.run(main())
