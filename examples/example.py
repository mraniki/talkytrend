"""
Provides example for talkytrend
"""

import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from talkytrend import TalkyTrend, __version__

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level="DEBUG"
)

logger = logging.getLogger(__name__)
logging.getLogger('TalkyTrend').setLevel(logging.DEBUG)


async def main():
    """Main"""
    while True:
        try:
            talky = TalkyTrend()
            #trend_plugin.monitor_assets()
            print(talky)
            logger.debug(
                "trend logger: %s version: %s",
                __name__,
                __version__)
            result = await talky.check_signal()
            print(result) #BUY
            result = await talky.fetch_key_events()
            print(result)
            monitor = await talky.scanner()
            print(monitor)

        except Exception as e:
            logger.error("error %s", e)


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
