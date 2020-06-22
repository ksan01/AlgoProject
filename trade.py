import alpaca_trade_api as tradeapi
from stock import Stock
from datetime import datetime, date
from time import sleep
import pytz
import statistics


API = tradeapi.REST()
SYMBOL = 'AAPL'
SYMBOLS = ['AAPL', 'MSFT', 'WMT', 'JNJ', 'CVX']
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

# Initializes the portfolio by creating an array of empty stock objects for the
# stocks in portfolio, using their ticker symbols as the names of the stock
def initStocks():
	stocks = [Stock(sym) for sym in SYMBOLS]
	return stocks

def printPortfolio(stocks):
	print("\nMy Portfolio")
	print("-------------------------------------------")
	for s in stocks:
		print(s.name)
	print("\n")

# Prints the current prices and the 1-hour moving averages of the stocks in 
# portfolio
def printStocks(stocks):

	tz = pytz.timezone('America/New_York') 
	time = datetime.now(tz).strftime("%H:%M:%S")
	print("\n\n" + time, "    Current Price   1-hour Average")
	print("-------------------------------------------")
	for stock in stocks:
		stock.printPrice()
	print("\n")

# Prints the summary of the trading session by printing the total number of BUY
# orders, the total number of SELL orders, the starting fund, the closing fund,
# and the calculated return
def printSummary(stock, money):

	today = date.today()
	print("\n\nEND OF DAY SUMMARY\n")
	print(today.strftime("%m/%d/%Y"), "       BUYS    SELLS")
	print("-------------------------------------------")
	stock.printTradeSummary()
	print("\nStarting Fund:", START)
	print("Closing Fund:", round(money, 3))
	ratio = ((money - START) / START) * 100
	print("Return:", str(round(ratio, 2)) + "%", "\n")

# Gets the current prices and 1-hour moving averages of each stock in portfolio
# Computes the z-score between the current price and 1-hour average of each stock
def getPrices(stocks):

	for stock in stocks:
		# get closing prices for each minute in the last hour to compute 1-hour 
		# moving average of the stock and get current price
		symbol      = stock.name
		barset      = API.get_barset(symbol, '1Min', limit = PERIOD)
		bars        = barset[symbol]
		prices      = [bar.c for bar in bars]
		stock.price = prices[-1]
		stock.avg   = round(statistics.mean(prices), 3)

		# compute z-score
		std = statistics.stdev(prices)
		stock.zscore = (stock.price - stock.avg) / std

# Executes BUY or SELL orders for the stock using the mean reversion strategy.
# Updates the fund, the number of stocks in possession, the number of BUY and 
# SELL orders for the stock accordingly 
def trade(stock, money):

	# if current price is greater than the 1-hour average by the amount of
	# SELL_FACTOR standard deviations, which is the z-score, sell the stock
	if (stock.zscore > SELL_FACTOR):
		if (stock.count > 0):
			stock.printTradeOrder(SELL)
			money += stock.price
			stock.count -= 1
			stock.sells += 1
		else:
			print("\nNo order for", stock.name + ", no stock to execute", 
				"SELL order\n")

	# if current price is lesset than the 1-hour average by the amount of
	# BUY_FACTOR standard deviations, which is the z-score, buy the stock
	elif (stock.zscore < BUY_FACTOR):
		# do not execute a BUY order if the order will decrease the fund by 50%
		if ((money - stock.price) > (START / 2)):
			stock.printTradeOrder(BUY)
			money -= stock.price
			stock.count += 1
			stock.buys += 1
		else:
			print("\nNo order for", stock.name + ", low fund to execute",
				"BUY order\n")

	# no BUY or SELL orders if BUY_FACTOR <= z-score <= SELL_FACTOR
	else:
		print("\nNo order for", stock.name, "\n")

	print("\nCurrent fund:", round(money, 3), "\n")
	return money




def main():

	stocks = initStocks()
	printPortfolio(stocks)
	getPrices(stocks)
	printStocks(stocks)

	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.\n")
		exit()

	print("\nStock Market is open, beginning trading\n")
	stocks = initStocks()
	printPortfolio(stocks)
	fund = START

	while (checkMarket()):
		getPrices(stock)
		printStocks(stock)
		fund = trade(stock, fund)

		print("\nRefreshing...\n\n\n")
		sleep(60)

	printSummary(stock, fund)


if __name__ == '__main__':
	main()