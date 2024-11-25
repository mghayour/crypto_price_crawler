import requests


def get_all_prices():
    url = "https://www.bitrue.com/kline-api/publicUSDT.json?command=returnTicker"
    response = requests.get(url,timeout=2)
    data = response.json()
    if str(data['code']) != '200':
        return None
    data = data['data']
    prices = []
    for key in data:
        if 'USDT' in key:
            prices.append((
                (key, data[key]['last'])
            ))
    return prices
