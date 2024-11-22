import requests


def get_price(coin):
    url = f"https://api.kraken.com/0/public/Ticker?pair={coin.upper()}USD"
    response = requests.get(url,timeout=1)
    data = response.json()
    return float(data['result'][list(data['result'].keys())[0]]['c'][0])

def get_all_prices():
    url = f"https://api.kraken.com/0/public/Ticker"
    response = requests.get(url,timeout=2)
    data = response.json()
    if 'result' not in data or type(data['result']) != dict:
        return None
    data = data['result']
    usd_prices = []
    for key in data:
        if key[-3:] == 'USD':
            usd_prices.append((
                (key[:-3], data[key]['c'][0])
            ))
    return usd_prices

