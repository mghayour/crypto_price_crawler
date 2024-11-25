import requests


def get_price(coin):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}USDT"
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['price'])


def get_all_prices():
    url = f"https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url,timeout=2)
    data = response.json()
    if type(data) is not list:
        return None
    prices = []
    for item in data:
        if 'USDT' in item['symbol']:
            prices.append((
                (item['symbol'], item['price'])
            ))
    return prices
