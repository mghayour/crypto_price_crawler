import requests


def get_price(symbol):
    url = (f"https://api.huobi.pro/market/detail/merged?symbol={symbol}usdt".format(symbol=symbol))
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['tick']['close'])
