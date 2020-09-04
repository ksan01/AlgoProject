import alpaca_trade_api as tradeapi
from stock import Stock
from datetime import datetime, date, time
from time import sleep
import pytz
import statistics
import requests
import xml.etree.ElementTree as ET


API = tradeapi.REST()
URL = "https://api.tradeking.com/v1/market/clock.xml"
SYMBOLS = ['AAPL', 'MSFT', 'FB', 'TSLA', 'GOOG', 'NFLX', 'ZM', 'BRK.B', 'JNJ', 'CVX']
BUY  = 'BUY'
SELL = 'SELL'
LINE = "-------------------------------------------"
PERIOD = 60
BUY_FACTOR = -1.0
SELL_FACTOR = 1.0
START = 100000


# Checks if the stock market is open
def checkMarket():
	res = requests.get(URL).content
	tree = ET.fromstring(res)
	result = tree.find('status/current')
	return (result.text == "open")

# Initializes the portfolio by creating an array of empty stock objects for the
# stocks in portfolio, using their ticker symbols as the names of the stock
def initPortfolio():
	stocks = [Stock(sym) for sym in SYMBOLS]
	return stocks

# Prints the symbols of each stock in the portfolio, and prints the starting fund
def printPortfolio(stocks):
	print("\nMy Portfolio")
	print(LINE)
	for stock in stocks:
		print(stock.name)
	print("\nStarting fund:", START, "\n")

# Prints the current prices and the 1-hour moving averages of the stocks in 
# the portfolio
def printPrices(stocks):

	tz = pytz.timezone('America/New_York') 
	time = datetime.now(tz).strftime("%H:%M:%S")
	print("\n\n" + time, "    Current Price   1-hour Average")
	print(LINE)
	for stock in stocks:
		stock.printPrice()
	print("\n")

# Prints the summary of the trading session by printing the total number of BUY
# orders and the total number of SELL orders for each stock. Prints the starting 
# fund, the closing fund, and the calculated return
def printSummary(stocks, money):

	today = date.today()
	print("\n\nEND OF DAY SUMMARY\n")
	print(today.strftime("%m/%d/%Y"), "       BUYS    SELLS")
	print(LINE)
	for stock in stocks:
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

# Checks if the stock has been indeed bought at a lower price than the 
# price at which it is about to be sold, which is sell_price.
def checkSellPrice(sell_price, bought_list):

	lower_prices = [elem for elem in bought_list if elem < sell_price]
	if (not lower_prices):
		return False
	else:
		# remove the price from price list of bought stocks
		bought_list.remove(lower_prices[0])
		return True

# Checks whether there is 30 minutes left for the stock market to close
def checkBuyTime():
	tz = pytz.timezone('America/New_York') 
	curr = datetime.now(tz).time()
	return (curr < time(15, 30))

# Executes BUY or SELL orders for each stock in portfolio using the mean 
# reversion strategy. Updates the fund, the number of stocks in possession, the
# number of BUY and SELL orders for the stocks accordingly 
def trade(stocks, money):

	for stock in stocks:

		# if the z-score between the current price and 1-hour average of the 
		# stocks is over the SELL_FACTOR, execute SELL order
		if (stock.zscore > SELL_FACTOR):
			if (stock.count > 0):
				if (checkSellPrice(stock.price, stock.bought)):
					stock.printTradeOrder(SELL)
					money += stock.price
					stock.count -= 1
					stock.sells += 1
				else:
					print("\nNo order for", stock.name, "\n")
			else:
				print("\nNo order for", stock.name + ", no stock to execute", 
					"SELL order\n")

		# if the z-score between the current price and 1-hour average of the 
		# stocks is under the BUY_FACTOR, execute BUY order
		elif (stock.zscore < BUY_FACTOR):
			# do not execute a BUY order if the market will close in 30 minutes
			if (checkBuyTime()):
				# do not execute a BUY order if the order will decrease the fund by 25%
				if ((money - stock.price) > (START * 0.75)):
					stock.printTradeOrder(BUY)
					money -= stock.price
					stock.count += 1
					stock.buys += 1
					stock.bought.append(stock.price)
				else:
					print("\nNo order for", stock.name + ", low fund to execute",
						"BUY order\n")
			else:
				print("\nNo order for", stock.name, "\n")

		# no BUY or SELL orders if BUY_FACTOR <= z-score <= SELL_FACTOR
		else:
			print("\nNo order for", stock.name, "\n")

	print("\nCurrent fund:", round(money, 3), "\n")
	return money


def main():

	if (not checkMarket()):
		print("\nStock Market is currently closed, exiting.\n")
		exit()

	print("\nStock Market is open, beginning trading\n")
	stocks = initPortfolio()
	printPortfolio(stocks)
	fund = START

	while (checkMarket()):
		getPrices(stocks)
		printPrices(stocks)
		fund = trade(stocks, fund)

		print("\nRefreshing...\n\n\n")
		sleep(60)

	printSummary(stocks, fund)


if __name__ == '__main__':
	main()