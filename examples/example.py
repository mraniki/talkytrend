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
    talky = TalkyTrend()
    print(talky)
    result = await talky.check_signal()
    print(result) #BUY
    result = await talky.fetch_key_events()
    print(result) # {'title': 'CPI m/m', 'country': 'USD', 'date': '2023-06-13T08:30:00-04:00', 'impact': 'High', 'forecast': '0.2%', 'previous': '0.4%'}
    monitor = await talky.scanner()
    # Key news: {'title': 'Fred Ryan to leave Washington Post after nine years as publisher',
    # 'url': 'https://www.washingtonpost.com/media/2023/06/12/fred-ryan-publisher-leaves-washington-post/'}


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
