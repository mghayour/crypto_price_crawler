import requests


def get_price(coin):
    url = f"https://api.gate.io/api2/1/ticker/{coin.lower()}_usdt"
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['last'])
