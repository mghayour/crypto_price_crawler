import requests


def get_price(coin):
    url = f"https://api.coinbase.com/v2/prices/{coin.upper()}-USD/spot"
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['data']['amount'])
