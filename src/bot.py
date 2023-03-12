##=============== VERSION =============

TTversion="📊🗿 TT Beta 0.0.1"

##=============== import  =============
##log
import logging
##env
import os
from dotenv import load_dotenv
import asyncio
import json, requests
#notification
import apprise
from apprise import NotifyFormat
#twelvedata
from twelvedata import TDClient
import time
#API
from fastapi import FastAPI, Header, HTTPException, Request
import uvicorn
import http
from prettytable import PrettyTable as pt

#🔧CONFIG
load_dotenv()
LOGLEVEL=os.getenv("LOGLEVEL", "INFO")
TDAPI=os.getenv("TDAPI", "TDAPI")
PORT=os.getenv("PORT", "8080")
HOST=os.getenv("HOST", "0.0.0.0")

#🧐LOGGING
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGLEVEL)
logger = logging.getLogger(__name__)
logger.info(msg=f"LOGLEVEL {LOGLEVEL}")

#🔗API
TDAPI=os.getenv("TDAPI", "TDAPI")
td = TDClient(apikey=TDAPI)

#🔁UTILS
from prettytable import PrettyTable
x = PrettyTable()

# #💬MESSAGING
# async def notify(msg):
#     if not msg:
#         return
#     apobj = apprise.Apprise()
#     try:
#         await apobj.async_notify(body=msg, body_format=NotifyFormat.HTML)
#     except Exception as e:
#         logger.warning(msg=f"{msg} not sent due to error: {e}")

#INDICATOR

async def supertrend_check(symbol, interval):
    ts = td.time_series(symbol=symbol, interval=interval, outputsize=2)
    supertrend_response = ts.with_supertrend().as_json()
    logger.debug(msg=f"supertrend_response {supertrend_response}")
    trend0 = supertrend_response[0]['supertrend']
    trend1 = supertrend_response[1]['supertrend']
    response = f"{symbol} {interval}\n"
    if trend0 > trend1:
        response += f"⬆️ 🐸 {trend0}"
    elif trend1 > trend0:
        response = f"⬇️ 🦑 {trend1}"
    else:
        response = f"↔️ {trend0}"
    logger.debug(msg=f"response {response}")
    return response




#CHECK
async def checker():
    global symboltrend
    while True:
        x.field_names = ["Symbol", "Trend"]
        x.add_rows(
            [
                ["EUR", await supertrend_check("EUR/USD","4h")],
                ["XAU", await supertrend_check("XAU/USD","4h")],
                ["BTC", await supertrend_check("BTC/USD","4h")],
            ]
        )
        symboltrend = x.get_string()
        time.sleep(3600)  # do work every one hour

#⛓️API
app = FastAPI(title="TALKYTREND",)

@app.on_event("startup")
def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(checker())
    logger.info(msg="Webserver started")

@app.on_event('shutdown')
async def shutdown_event():
    logger.info('Webserver shutting down...')

@app.get("/")
def root():
    return {f"Bot is online {TTversion}\n"}

@app.get("/trend")
def trend():
    return {f"symboltrend {x.get_string()}\n"}

@app.get("/health")
def health_check():
    logger.info(msg="Healthcheck_Ping")
    return {f"Bot is online {TTversion}"}

#🙊TALKYTREND
if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)


