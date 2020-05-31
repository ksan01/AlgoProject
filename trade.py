import alpaca_trade_api as tradeapi
from stock import Stock
from datetime import datetime
import pytz
api = tradeapi.REST()
name = 'APPL'


def checkMarket():
	clock = api.get_clock()
	return clock.is_open

def initStock():
	return Stock(name)

def main():

	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.\n")
		exit()

	print("\nStock Market is open\n")
	stock = initStock()

	while (checkMarket()):
		print("\nMarket Open\n")
		sleep(60)

if __name__ == '__main__':
	main()