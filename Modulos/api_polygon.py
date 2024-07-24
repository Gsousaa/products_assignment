from fastapi import  HTTPException
from datetime import datetime, timedelta
from .prep_values import get_last_weekday
import requests
import os

def polygon(symbol:str):
    max_attempts = 5
    attempts = 0
    current_date = datetime.now()
    while attempts < max_attempts:
        
        date = get_last_weekday(current_date)
        url = os.getenv("URL_POLYGON")+f"{symbol}/{date}"
        headers = {"Authorization": f"Bearer "+str(os.getenv("TOKEN_API"))}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            stock_data = response.json()        
            return stock_data,date
        else:
            current_date = current_date - timedelta(days=1)
            attempts += 1
    raise HTTPException(status_code=404, detail="Error fetching stock data")