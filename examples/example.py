"""
Provides example for talkytrend
"""

import asyncio

import uvicorn
from fastapi import FastAPI

from talkytrend import TalkyTrend


async def main():
    """Main"""
    talky = TalkyTrend()
    print(talky)

    trend = await talky.check_signal()
    print("trend:\n",trend)
    # signal:
    #  +--------+----+
    # | Asset  | 4h |
    # +--------+----+
    # | EURUSD | 🔼 |

    feed = await talky.fetch_key_feed()
    print("feed:\n",feed)
    #  📰 <a href='https://www.zerohedge.com/political/one-third-seattle-residents-may-flee-city-over-crime-costs'>
    # One-Third Of Seattle Residents May Flee City Over Crime, Costs</a>
    events = await talky.fetch_key_events()
    print("events:\n",events) 
    # 💬 Core PPI m/m
    # ⏰ 2023-06-14T08:30:00-04:00
    fomc_day = await talky.check_fomc()
    print("is it FOMC today:\n",fomc_day)
    #False

    async for message in talky.scanner():
        print("scanner:\n", message)
        await talky.allow_scanning(enable=False)
        # scanner:
        #  💬 FOMC Member Barr Speaks
        # ⏰ 2023-07-10T10:00:00-04:00
        #  📰 <a href='https://www.zerohedge.com/political/one-third-seattle-residents-may-flee-city-over-crime-costs'>
        # One-Third Of Seattle Residents May Flee City Over Crime, Costs</a>
        #  <table>
        #     <thead>
        #         <tr>
        #             <th>Asset</th>
        #             <th>4h</th>
        #         </tr>
        #     </thead>
        #     <tbody>
        #         <tr>
        #             <td>EURUSD</td>
        #             <td>🔼</td>
        #         </tr>
        #         <tr>
        #             <td>BTCUSD</td>
        #             <td>🔽</td>
        #         </tr>
        #     </tbody>
        # </table>

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
