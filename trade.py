import alpaca_trade_api as tradeapi
from stock import Stock
from datetime import datetime
from time import sleep
import pytz
import statistics


API = tradeapi.REST()
SYMBOL = 'AAPL'
BUY  = 'BUY'
SELL = 'SELL'

def checkMarket():
	clock = API.get_clock()
	return clock.is_open

def initStock():
	return Stock(SYMBOL)

def printStock(stock):
	tz = pytz.timezone('America/New_York') 
	time = datetime.now(tz).strftime("%H:%M:%S")
	print("\n\n" + time, "    Current Price   1-hour Average")
	print("-------------------------------------------")
	stock.printPrice()

def getPrices(stock):
	# get current price of the stock
	last_trade  = API.get_last_trade(SYMBOL)
	stock.price = last_trade.price 

	# get closing prices for each minute in the last hour
	barset      = API.get_barset(SYMBOL, '1Min', limit=60)
	bars        = barset[SYMBOL]
	prices      = [bar.c for bar in bars]
	stock.avg   = round(statistics.mean(prices), 2)

	# compute z-score
	std = statistics.stdev(prices)
	stock.zscore = (stock.price - stock.avg) / std
	print(stock.zscore)

def main():
	
	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.")
		exit()

	print("\nStock Market is open, beginning trading\n")
	stock = initStock()

	while (checkMarket()):
		getPrices(stock)
		printStock(stock)

		print("\nRefreshing...\n")
		sleep(10)

if __name__ == '__main__':
	main()