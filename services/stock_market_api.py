from http import HTTPStatus
import requests
from datetime import datetime, date

from configs.settings import ASSETS_API_URL, ASSETS_API_KEY

def get_live_quote_price(symbol: str) -> str | None:
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': f'{symbol}.SAO',
        'apikey': ASSETS_API_KEY,
    }
    
    response = requests.get(f'{ASSETS_API_URL}/query', params=params)
    if response.status_code != HTTPStatus.OK:
        return 
    
    response = response.json()
    quote = response['Global Quote']
    if not quote:
        return
    last_trading_date = quote['07. latest trading day']
    
    if datetime.strptime(last_trading_date, '%Y-%m-%d').date() == date.today():
        return quote['05. price']

    return
