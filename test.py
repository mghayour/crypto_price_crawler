from api import kraken as exchange


data = exchange.get_all_prices()
print(data)