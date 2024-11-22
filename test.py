from api import binance as exchange


data = exchange.get_all_prices()
print(data)