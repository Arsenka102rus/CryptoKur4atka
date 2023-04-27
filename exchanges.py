import ccxt


def coin_price(coin='BTC'):
    usdt = 'USDT'
    try:
        exchange = ccxt.binance()
        symbol = coin + "/" + usdt
        ticker = exchange.fetchTicker(symbol)
        return ticker['last']
    except Exception as error:
        print(error)


print(coin_price('ETH'))