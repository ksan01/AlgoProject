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
PERIOD = 60
BUY_FACTOR = -1.0
SELL_FACTOR = 1.0
START = 10000


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
	print("\n")

# Prints the summary of the trading session by printing the total number of BUY
# orders, the total number of SELL orders, the starting fund, the closing fund,
# and the calculated return
def printSummary(stock, money):
	print("\n\nEND OF DAY SUMMARY |  BUYS   SELLS")
	print("-------------------------------------------")
	stock.printTradeSummary()
	print("\nStarting Fund:", START)
	print("Closing Fund:", money)
	ratio = ((money - START) / START) * 100
	print("Return:", str(round(ratio, 2)) + "%")

# Exits program if the current fund is up to 25% lower than the starting fund
def checkLoss(money):

	ratio = money / START
	loss = ((money - START) / START) * 100
	if (ratio <= 0.75):
		print("\nLosses up to", str(round(loss, 2)) + "%", "exiting program.")
		exit()

# Gets the current price and 1-hour moving average of the stock. Computes the
# z-score between the current price and 1-hour average of the stock
def getPrices(stock):

	# get current price of the stock
	last_trade  = API.get_last_trade(SYMBOL)
	stock.price = last_trade.price 

	# get closing prices for each minute in the last hour 
	# to compute 1-hour moving average of the stock
	barset      = API.get_barset(SYMBOL, '1Min', limit = PERIOD)
	bars        = barset[SYMBOL]
	prices      = [bar.c for bar in bars]
	stock.avg   = round(statistics.mean(prices), 2)

	# compute z-score
	std = statistics.stdev(prices)
	stock.zscore = (stock.price - stock.avg) / std
	print(stock.zscore)

# Executes BUY or SELL orders for the stock using the mean reversion strategy.
# Updates the fund and number of stocks in possession accordingly to these 
# orders
def trade(stock, money):

	# if current price is greater than the 1-hour average by the amount of
	# SELL_FACTOR standard deviations, which is the z-score, sell the stock
	if (stock.zscore > SELL_FACTOR):
		if (stock.count > 0):
			print(stock.zscore)
			stock.printTradeOrder(SELL)
			money += stock.price
			print("count before", stock.count)
			stock.count -= 1
			print("count after", stock.count)
			stock.sells += 1
		else:
			print("\nNo order for", stock.name, "\n")

	# if current price is lesset than the 1-hour average by the amount of
	# BUY_FACTOR standard deviations, which is the z-score, buy the stock
	elif (stock.zscore < BUY_FACTOR):
		print(stock.zscore)
		stock.printTradeOrder(BUY)
		money -= stock.price
		print("count before", stock.count)
		stock.count += 1
		print("count after", stock.count)
		stock.buys += 1

	# No BUY or SELL orders if BUY_FACTOR <= z-score <= SELL_FACTOR
	else:
		print("\nNo order for", stock.name, "\n")

	print("Current fund:", money, "\n")
	return money

def main():
	
	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.")
		exit()

	print("\nStock Market is open, beginning trading\n")
	stock = initStock()
	fund = START

	while (checkMarket()):
		getPrices(stock)
		printStock(stock)
		fund = trade(stock, fund)
		checkLoss(fund)

		print("\nRefreshing...\n\n\n")
		# TODO: change to 60s 
		sleep(10)

	printSummary(stock, fund)


if __name__ == '__main__':
	main()