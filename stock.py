from datetime import datetime
import pytz

'''
Representation of a Stock object

 name: ticker symbol of stock
 price: current price of stock
 avg:  moving average of stock
 zscore: z-score between price and avg
 count: number of stocks in possesion
 buys: number of BUY orders for the stock
 sells: number of SELL orders for the stock
 boughtStocks: a list holding the prices that the stock has been bought. This 
 			   attribute was added to keep track of buy prices of the stocks as 
 			   the mean reversion algorithm can sometimes cause the program to 
 			   sell the stock at a lower price than it has been bought.


 printPrice: prints the ticker symbol, price, and 1-hour average of a single
             stock so that the printed variables are justified properly to
             print a nicely aligned table 

 printTradeOrder: prints the trade order for a single stock, which includes the 
			  	  action (BUY/SELL), the ticker symbol of the stock, traded 
				  price, traded time, 1-hour moving average of the stock, and 
				  the z-score between the stock's price and 1-hour moving 
 			      average 

 printTradeSummary: prints the ticker symbol, number of BUY orders, number of
		     	    SELL orders of a single stock so that the printed variables 
		     	    are justified properly to print a nicely aligned table 
'''

class Stock:

	def __init__(self, symbol):
		self.name   = symbol
		self.price  = 0
		self.avg    = 0
		self.zscore = 0
		self.count  = 0
		self.buys   = 0
		self.sells  = 0
		self.boughtStocks = []

	def printPrice(self):
		print(self.name.ljust(4), "         ", str(self.price).ljust(8),  
			"       ", str(self.avg).ljust(8))

	def printTradeOrder(self, act):
		tz = pytz.timezone('America/New_York') 
		time = datetime.now(tz).strftime("- %H:%M:%S")
		print("\n\n" + act, "order for", self.name, "at",self.price, time)
		print("-------------------------------------------")
		print("Price:", self.price)
		print("1-hour Average:", self.avg)
		print("Z-Score:", round(self.zscore, 3), "\n")

	def printTradeSummary(self):
		print(self.name.ljust(4), "     	  ", str(self.buys).ljust(3)
			, "    ", str(self.sells).ljust(3))






