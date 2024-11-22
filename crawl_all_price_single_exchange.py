from api import bitrue, binance, kraken
from api import coinbase, bitfinex, kucoin, gateio, huobi, okx
import argparse
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


exchanges = {
    "bitrue": bitrue, 
    "binance": binance, 
    "kraken": kraken, 
    "coinbase": coinbase, 
    "bitfinex": bitfinex, 
    "kucoin": kucoin, 
    "gateio": gateio, 
    "huobi": huobi, 
    "okx": okx
}
interesting_coins = ["btc","eth","bnb","ltc","ada","dot","1inch","uni","xrp","ens","sol","ton"]
exchange_who_support_all_price_list = ["bitrue", "binance", "kraken"]


def fetch_price(get_price_func, coin):
    try:
        price = get_price_func(coin)
        return coin, price, None
    except Exception as e:
        return coin, None, str(e)


def get_all_prices(exchange_name):
    if exchange_name in exchange_who_support_all_price_list:
        return exchanges[exchange_name].get_all_prices()

    get_price_func = exchanges[exchange_name].get_price
    with ThreadPoolExecutor(max_workers=len(interesting_coins)) as executor:
        futures = {
            executor.submit(fetch_price, exchange_name, get_price_func, coin): coin for coin in interesting_coins
        }
        results = [future.result() for future in futures]
    valid_results = [(coin, price) for coin, price, error in results if price is not None]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cryptocurrency crawling API client')
    parser.add_argument('--exchange', help='Exchange name')
    args = parser.parse_args()
    if args.exchange not in exchanges:
        raise ValueError("Unsupported exchange: {}".format(args.exchange))

    prices = get_all_prices(args.exchange)
    print(prices)
