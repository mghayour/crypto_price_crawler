import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from api import binance, coinbase, bitfinex, kucoin, gateio, kraken, huobi, okx
import argparse


def fetch_price(exchange, get_price_func, coin):
    try:
        price = get_price_func(coin)
        return exchange, price, None
    except Exception as e:
        return exchange, None, str(e)


def get_coin_price(coin):
    coin = coin.lower()

    # All available exchanges
    exchanges = {
        'Coinbase': coinbase.get_price,
        'Bitfinex': bitfinex.get_price,
        'Gate.io': gateio.get_price,
        'Kraken': kraken.get_price,
        'Binance': binance.get_price,
        'KuCoin': kucoin.get_price,
        'Huobi': huobi.get_price,
        'OKX': okx.get_price
    }

    with ThreadPoolExecutor(max_workers=len(exchanges)) as executor:
        futures = {executor.submit(fetch_price, exchange, get_price_func, coin): exchange for
                    exchange, get_price_func in exchanges.items()}
        results = [future.result() for future in futures]
    valid_results = [(exchange, price) for exchange, price, error in results if price is not None]

    return valid_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cryptocurrency crawling API client')
    parser.add_argument('--coin', default="btc", help='Coin name')
    args = parser.parse_args()
    coin = args.coin
    prices = get_coin_price(coin)
    print(f"Prices for {coin.upper()}: {prices}")
    


