import requests
from config import CG_API


def get_data(timeframe='h1'):
    url = f"https://open-api.coinglass.com/public/v2/long_short?time_type={timeframe}&symbol=BTC"

    headers = {
        "accept": "application/json",
        "coinglassSecret": CG_API
    }
    try:
        response = requests.get(url, headers=headers).json()
        return response['data'][0]['longRate'], response['data'][0]['shortRate']
    except Exception as error:
        return error
