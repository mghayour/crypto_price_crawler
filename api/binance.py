import requests


def get_price(coin):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}USDT"
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['price'])
