import requests


def get_all_prices():
    url = "https://www.bitrue.com/kline-api/publicUSDT.json?command=returnTicker"
    response = requests.get(url,timeout=2)
    data = response.json()
    if str(data['code']) != '200':
        return None
    return [(key.split("_")[0], data['data'][key]['last']) for key in data['data']]
