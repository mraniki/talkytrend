"""
Provides example for talkytrend
"""

import asyncio
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger

from talkytrend import TalkyTrend

logger.remove()
logger.add(sys.stderr, level="INFO")


async def main():
    """Main"""
    talky = TalkyTrend()
    print(talky)

    instrument_info = await talky.fetch_instrument_info()
    print("instrument_info:\n",instrument_info)

    trend = await talky.fetch_signal()
    print("trend:\n",trend)
    # signal:
    #  +--------+----+
    # | Asset  | 4h |
    # +--------+----+
    # | EURUSD | 🔼 |

    feed = await talky.fetch_feed()
    print("feed:\n",feed)
    #  📰 <a href='https://www.zerohedge.com/political/one-third-seattle-residents-may-flee-city-over-crime-costs'>
    # One-Third Of Seattle Residents May Flee City Over Crime, Costs</a>
    events = await talky.fetch_event()
    print("events:\n",events) 
    # 💬 Core PPI m/m
    # ⏰ 2023-06-14T08:30:00-04:00
    fomc_day = await talky.check_fomc()
    print("is it FOMC today:\n",fomc_day)
    #False

    monitor = await talky.monitor()
    print("monitor:\n",monitor)

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
    uvicorn.run(app, host="0.0.0.0", port=8089)
