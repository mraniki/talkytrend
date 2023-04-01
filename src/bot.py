import yfinance as yf
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from prettytable import PrettyTable
from apprise import Apprise
from colorama import Fore, Style
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
timeframe_minutes = os.getenv("TIMEFRAME_MINUTES",'4 *60')
newsapikey=os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=newsapikey)

instruments = ['EURUSD=X', 'GC=F', 'CL=F', 'BTC-USD']


# Create an empty table with the columns we want to display
table = PrettyTable(['Symbol', 'Supertrend'])

# Connect to the News API
newsapi = NewsApiClient(api_key='YOUR_NEWS_API_KEY')

# Get the top market news headline
top_headlines = newsapi.get_top_headlines(q='market', category='business', country='us', language='en')
if top_headlines['totalResults'] > 0:
    news_headline = top_headlines['articles'][0]['title']
else:
    news_headline = ''

# Set the news headline as the header of the table
table.title = news_headline

# Loop through each instrument and calculate the supertrend
for symbol in instruments:
    # Get the historical data for the symbol
    data = yf.download(symbol, period='1d', interval='1m')
    
    # Calculate the supertrend using the Supertrend indicator
    data['atr'] = data['High'] - data['Low']
    data['basic_ub'] = (data['High'] + data['Low']) / 2 + (3 * data['atr'] / timeframe_minutes)
    data['basic_lb'] = (data['High'] + data['Low']) / 2 - (3 * data['atr'] / timeframe_minutes)
    data['final_ub'] = 0.00
    data['final_lb'] = 0.00
    for i in range(timeframe_minutes, len(data)):
        data['final_ub'].iloc[i] = data['basic_ub'].iloc[i] if data['basic_ub'].iloc[i] < data['final_ub'].iloc[i - 1] or data['Close'].iloc[i - timeframe_minutes] > data['final_ub'].iloc[i - 1] else data['final_ub'].iloc[i - 1]
        data['final_lb'].iloc[i] = data['basic_lb'].iloc[i] if data['basic_lb'].iloc[i] > data['final_lb'].iloc[i - 1] or data['Close'].iloc[i - timeframe_minutes] < data['final_lb'].iloc[i - 1] else data['final_lb'].iloc[i - 1]
    data['supertrend'] = data['final_ub'] if data['final_ub'].iloc[-1] < data['Close'].iloc[-1] else data['final_lb']
    
    # Determine the emoji and color based on whether the supertrend is up or down
    if data['supertrend'].iloc[-1] > data['Close'].iloc[-1]:
        emoji = '🔴'
        color = Fore.RED
    else:
        emoji = '🟢'
        color = Fore.GREEN
    
    # Add the symbol and supertrend to the table with color
    table.add_row([symbol, f'{color}{round(data["supertrend"].iloc[-1], 2)}{Style.RESET_ALL}'])

# Create a FastAPI app
app = FastAPI()

# Define a route to return the HTML version of the table
@app.get('/', response_class=HTMLResponse)
async def get_table_html():
    return f'<html><body><pre>{table}</pre></body></html>'

# Define a route to return the JSON version of the table
@app.get('/api/table', response_class=JSONResponse)
async def get_table_json():
    data = []
    for row in table:
        data.append({'Symbol': row[0], 'Supertrend': row[1]})
    return {'data': data}

# Send the table to Discord and Telegram
apobj = Apprise()
apobj.add('discord://YOUR_DISCORD_WEBHOOK_URL')
apobj.add('telegram://YOUR_TELEGRAM_BOT_TOKEN/YOUR_TELEGRAM_CHAT_ID')
message = f'```{table}```'
apobj.notify(title='Supertrend Table', body=message)