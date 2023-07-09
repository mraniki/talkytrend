"""
Provides example for talkytrend
"""

import asyncio
# import logging

import uvicorn
from fastapi import FastAPI
from talkytrend import TalkyTrend, __version__

# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     level="DEBUG"
# )
# logger = logging.getLogger(__name__)
# logging.getLogger('TalkyTrend').setLevel(logging.DEBUG)
# logging.getLogger('urllib3').setLevel(logging.WARNING)

async def main():
    """Main"""
    talky = TalkyTrend()
    # print(talky)
    #signal = await talky.check_signal()
    #print("signal:\n",signal) 
    #{'EURUSD': {'4h': 'STRONG_BUY'}, 'BTCUSD': {'4h': 'NEUTRAL'}}

    feed = await talky.fetch_key_feed()
    print("feed:\n",feed) 
    #events = await talky.fetch_key_events()
    #print("events:\n",events) 
    # 💬 Core PPI m/m
    # ⏰ 2023-06-14T08:30:00-04:00
    # fomc_day = await talky.check_fomc()
    # print(fomc_day)
    #True
    # while True:
    #     async for message in talky.scanner():
    #         print("scanner:\n", message)
            #💬 Core PPI m/m
            #⏰ 2023-06-14T08:30:00-04:00
            #{'title': "Bud Light loses its title as America's top-selling beer", 'url': 'https://edition.cnn.com/2023/06/14/business/bud-light-modelo-top-selling-may-sales/index.html'}
            # |    Asset   |    4h   |
            # |:----------:|:-------:|
            # |   EURUSD   |    ⏫   |
            # |   BTCUSD   |    ▶️    |


app = FastAPI()


@app.on_event("startup")
async def start():
    """startup"""
    asyncio.create_task(main())


@app.get("/")
def read_root():
    """root"""
    return {"online"}


@app.get("/health")
def health_check():
    """healthcheck"""
    return {"online"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
