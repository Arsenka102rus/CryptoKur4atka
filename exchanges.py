import requests

USDT = 'USDT'


def binance_get_price(coin='BTC'):
    symbol = coin + USDT
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}').json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response['price']), 2)
    return -1


def coinbase_get_price(coin='BTC'):
    symbol = coin + "-" + "USD"
    try:
        response = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}/spot").json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response['data']['amount']), 2)
    return -1


def kraken_get_price(coin='BTC'):
    symbol = coin + USDT
    try:
        response = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={symbol}").json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        # return round(float(response['amount']), 2)
        if coin != 'BTC':
            print(response['result'][symbol]['c'][0])
            return response['result'][symbol]['c'][0]
        return round(float(response['result']['XBTUSDT']['c'][0]), 2)
    return -1


def kucoin_get_price(coin='BTC'):
    symbol = coin + "-" + USDT
    try:
        response = requests.get(f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}").json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response['data']['price']), 2)
    return -1


def bybit_get_price(coin='BTC'):
    symbol = coin + USDT
    try:
        response = requests.get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}").json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response['result']['list'][0]['lastPrice']), 2)
    return -1


def bitfinex_get_price(coin='BTC'):
    symbol = coin + "USD"
    try:
        url = "https://api-pub.bitfinex.com/v2/"
        response = requests.get(url + f'ticker/t{symbol}').json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response[6]), 2)
    return -1


def gateio_get_price(coin="BTC"):
    symbol = coin + "_" + USDT
    try:
        url = "https://api.gateio.ws/api/v4"
        params = {
            'currency_pair': symbol
        }
        response = requests.get(url + f'/spot/tickers', params=params).json()
    except Exception as error:
        print(f"Ошибка {error} при парсинге")
        response = 'ERROR'
    if response != 'ERROR':
        return round(float(response[0]['last']), 2)
    return -1


def all_ex_price(coin='BTC'):
    total = {
        'binance': binance_get_price(coin),
        'coinbase': coinbase_get_price(coin),
        'kraken': kraken_get_price(coin),
        'kucoin': kucoin_get_price(coin),
        'bybit': bybit_get_price(coin),
        'bitfinex': bitfinex_get_price(coin),
        'gateio': gateio_get_price(coin)
    }
    return total


def main():
    print(all_ex_price())


if __name__ == '__main__':
    main()
