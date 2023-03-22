##=============== VERSION =============

TTversion="📊🗿 TT Beta 0.0.2"

##=============== import  =============
##log
import logging
##env
import os
from dotenv import load_dotenv
import asyncio
import json, requests
#Table
import pandas as pd
from prettytable import PrettyTable as pt
#notification
import apprise
from apprise import NotifyFormat

from microdot import Microdot
#twelvedata.com
from twelvedata import TDClient
import time
#finnhub.io
import finnhub
#Federal Reserve Bank of St. Louis
from fredapi import Fred


#🔧CONFIG
load_dotenv()
LOGLEVEL=os.getenv("LOGLEVEL", "INFO")
TDAPI=os.getenv("TDAPI", "TDAPI")
FNAPI=os.getenv("FNAPI", "FNAPI")
FRAPI=os.getenv("FRAPI", "FRAPI")
PORT=os.getenv("PORT", "8080")
HOST=os.getenv("HOST", "0.0.0.0")

#🧐LOGGING
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOGLEVEL)
logger = logging.getLogger(__name__)
logger.info(msg=f"LOGLEVEL {LOGLEVEL}")

#🔗API
td = TDClient(apikey=TDAPI)
fn = finnhub.Client(api_key=FNAPI)
fred = Fred(api_key=FRAPI)

#🔗APITEST
dataSP500 = fred.get_series('SP500')

#🔁UTILS
from prettytable import PrettyTable
x = PrettyTable()


def retrieve_url_json(url,params=None):
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(url,params =params,headers=headers)
    logger.debug(msg=f"retrieve_url_json {response}")
    return response.json()


# #💬MESSAGING
# #APPRISE INSTANCE
# # apobj = apprise.Apprise()
# # config = apprise.AppriseConfig()
# # APPRISECFG=os.getenv("APPRISE", "/config/config.yml")
# # config.add(APPRISECFG)
# # apobj.add(config)

# # #APPRISE NOTIFICATION
# # async def notify(msg):
# #     if not msg:
# #         return
# #     try:
# #         await apobj.async_notify(body=msg, body_format=NotifyFormat.HTML)
# #     except Exception as e:
# #         logger.warning(msg=f"{msg} not sent due to error: {e}")

#INDICATOR
def indicator_supertrend(symbol, interval):
    ts = td.time_series(symbol=symbol, interval=interval, outputsize=2)
    supertrend_response = ts.with_supertrend().as_json()
    logger.debug(msg=f"supertrend_response {supertrend_response}")
    trend0 = supertrend_response[0]['supertrend']
    trend1 = supertrend_response[1]['supertrend']
    if trend0 > trend1:
        response = f"🟢⬆️ {trend0}"
    elif trend1 > trend0:
        response = f"🔴⬇️ {trend1}"
    else:
        response = f"🟡↔️ {trend0}"
    logger.debug(msg=f"response {response}")
    return response

#VIEWER
def viewer_news():
    news= fn.general_news('general', min_id=0)
    logger.debug(msg=f"news {news}")
    df = pd.read_json(news)
    df.to_csv()
    for keyval in news:
        if (keyval['category'] == 'top news'):
            return f"<a href={keyval['url']}>{keyval['headline']}"

            
            
def viewer_supertrend():
    global symboltrend
    news= fn.general_news('general', min_id=0)
    x.field_names = ["Symbol", "Trend"]
    x.align = "r"
    x.add_rows(
        [
            ["EUR",  indicator_supertrend("EUR/USD","4h")],
            ["XAU",  indicator_supertrend("XAU/USD","4h")],
            ["BTC",  indicator_supertrend("BTC/USD","4h")],
        ]
    )
    symboltrend = x.get_string()
    logger.info(msg=f"symboltrend {symboltrend}")


app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Talky</title>
    </head>
    <body>
        <div>Talky Trend</h1>
            <p>Menu</p>
            <p><a href="/trend">Trend</a></p>
            <p><a href="/news">News</a></p>
            <p><a href="/shutdown">Shutdown the server</a></p>
        </div>
        <img src="https://user-images.githubusercontent.com/8766259/226854338-e900f69e-d884-4a9a-90b1-b3dde7711b31.png" alt="Talky Trend" width="300" height="300"> 
    </body>
</html>
'''

@app.route('/')
def hello(request):
    return htmldoc, 200, {'Content-Type': 'text/html'}

@app.route('/trend')
def trend(request):
    return viewer_supertrend(), 200, {'Content-Type': 'text/html'}

@app.route('/news')
def news(request):
    return viewer_news(), 200, {'Content-Type': 'text/html'}

@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

#🙊TALKYTRADER
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)


