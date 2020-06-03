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
BUY_FACTOR = -1.0
SELL_FACTOR = 1.0

# Checks if the stock market is open
def checkMarket():
	clock = API.get_clock()
	return clock.is_open

# Initializes an empty stock object using ticker symbol as the name of the stock
def initStock():
	return Stock(SYMBOL)

# Prints the current price and the 1-hour moving average of the stock
def printStock(stock):

	tz = pytz.timezone('America/New_York') 
	time = datetime.now(tz).strftime("%H:%M:%S")
	print("\n\n" + time, "    Current Price   1-hour Average")
	print("-------------------------------------------")
	stock.printPrice()

# Gets the current price and 1-hour moving average of the stock. Computes the
# z-score between the current price and 1-hour average of the stock
def getPrices(stock):

	# get current price of the stock
	last_trade  = API.get_last_trade(SYMBOL)
	stock.price = last_trade.price 

	# get closing prices for each minute in the last hour 
	# to compute 1-hour moving average of the stock
	barset      = API.get_barset(SYMBOL, '1Min', limit=60)
	bars        = barset[SYMBOL]
	prices      = [bar.c for bar in bars]
	stock.avg   = round(statistics.mean(prices), 2)

	# compute z-score
	std = statistics.stdev(prices)
	stock.zscore = (stock.price - stock.avg) / std
	print(stock.zscore)

# Executes BUY or SELL orders for the stock using the mean reversion strategy
def trade(stock):

	# if current price is greater than the 1-hour average by the amount of
	# SELL_FACTOR standard deviations, which is the z-score, sell the stock
	if (stock.zscore > SELL_FACTOR):
		if (stock.count > 0):
			print(stock.zscore)
			stock.printTrade(SELL)
		else:
			print("\nNo order for", stock.name, "\n")

	# if current price is lesset than the 1-hour average by the amount of
	# BUY_FACTOR standard deviations, which is the z-score, buy the stock
	elif (stock.zscore < BUY_FACTOR):
		print(stock.zscore)
		stock.printTrade(BUY)

	# No BUY or SELL orders if BUY_FACTOR < z-score < SELL_FACTOR
	else:
		print("\nNo order for", stock.name, "\n")

def main():
	
	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.")
		exit()

	print("\nStock Market is open, beginning trading\n")
	stock = initStock()

	while (checkMarket()):
		getPrices(stock)
		printStock(stock)
		trade(stock)

		print("\nRefreshing...\n")
		# TODO: change to 60s 
		sleep(10)



if __name__ == '__main__':
	main()