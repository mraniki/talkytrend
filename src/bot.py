import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
import uvicorn
import gspread
import pandas as pd


load_dotenv()
GSHEET=os.getenv("GSHEET")
PORT=os.getenv("PORT", "8080")
HOST=os.getenv("HOST", "0.0.0.0")

def get_dashboard():
    gc = gspread.service_account(filename='config/service_account.json')
    book = gc.open_by_key(GSHEET)
    dashboard = book.get_worksheet(0)
    df = pd.DataFrame(dashboard.get_all_values())
    print(df)
    return df

app = FastAPI()

@app.get("/")
def read_root():
    return  get_dashboard()

if __name__ == '__main__':
    uvicorn.run("bot:app", host=HOST, port=PORT, reload=True)