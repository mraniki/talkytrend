"""
Provides example for talkytrend
"""

import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from talkytrend import TrendPlugin, __version__

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level="DEBUG"
)

logger = logging.getLogger(__name__)
logging.getLogger('TTREND').setLevel(logging.DEBUG)


async def main():
    """Main"""
    while True:
        try:
            trend_plugin = TrendPlugin()
            #trend_plugin.monitor_assets()
            print(trend_plugin)
            logger.debug(
                "trend_plugin logger: %s version: %s",
                __name__,
                __version__)

                

            await asyncio.sleep(7200)

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
    uvicorn.run(app, host="0.0.0.0", port=8080)
