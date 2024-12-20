from api import bitrue, binance, kraken
from api import coinbase, bitfinex, kucoin, gateio, huobi, okx
import argparse
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
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
        try:
            return exchanges[exchange_name].get_all_prices()
        except Exception as e:
            return []

    get_price_func = exchanges[exchange_name].get_price
    with ThreadPoolExecutor(max_workers=len(interesting_coins)) as executor:
        futures = {
            executor.submit(fetch_price, get_price_func, coin): coin for coin in interesting_coins
        }
        results = [future.result() for future in futures]
    valid_results = [(coin, price) for coin, price, error in results if price is not None]
    return valid_results

def get_and_save_all_prices(exchange, output):
    start_time = time.time()
    prices = get_all_prices(exchange)
    end_time = time.time()
    print("get_all_prices time", end_time-start_time)
    price_dict = {}
    price_dict['timestamp']=(end_time+start_time)/2
    for coin, price in prices:
        price_dict[coin] = price
    
    if output == "":
        print(json.dumps(price_dict, indent=2))
    else:
        with open(output, 'a') as f:
            json.dump(price_dict, f)
            f.write('\n')

def replace_placeholder_in_filename(filename,exchange):
    today_date = datetime.utcnow().strftime('%Y%m%d')
    filename = filename.replace("<TODAY>", today_date)
    filename = filename.replace("<EXCHANGE>", exchange)
    return filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cryptocurrency crawling API client')
    parser.add_argument('--exchange', help='Exchange name')
    parser.add_argument('--output', default="", help='Exchange name')
    parser.add_argument('--count', default=1, type=int, help='Number of times to fetch')
    parser.add_argument('--delay', default=0, type=int, help='delay seconds between sampling')
    args = parser.parse_args()
    if args.exchange not in exchanges:
        raise ValueError("Unsupported exchange: {}".format(args.exchange))

    output = replace_placeholder_in_filename(args.output, args.exchange)
    start_time = time.time()
    needed_times = [start_time+i*args.delay for i in range(args.count)]

    for i in range(args.count):
        start_time = needed_times[i]
        the_time = time.time()
        time.sleep(max(0, start_time-the_time))
        get_and_save_all_prices(args.exchange, output)

    

