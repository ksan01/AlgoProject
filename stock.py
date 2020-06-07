from datetime import datetime
import pytz

'''
Representation of a Stock object

 name: ticker symbol of stock
 price: last trade price of stock
 avg:  moving average of stock
 zscore: z-score between price and avg
 count: number of stocks in possesion
 buys: number of BUY orders for the stock
 sells: number of SELL orders for the stock

 printPrice: prints the ticker symbol, price, and 1-hour average of a single
             stock in a table-like format

 printTradeOrder: prints the trade order for a single stock, which includes the 
			  	  action (BUY/SELL), the ticker symbol of the stock, traded 
				  price, traded time, 1-hour moving average of the stock, and 
				  the z-score between the stock's price and 1-hour moving 
 			      average 

 printTradeSummary: prints the ticker symbol, number of BUY orders, number of
		     	    SELL orders of a single stock in a table-like format
'''

class Stock:

	def __init__(self, name):
		self.name   = name
		self.price  = 0
		self.avg    = 0
		self.zscore = 0
		self.count  = 0
		self.buys   = 0
		self.sells  = 0

	def printPrice(self):
		print(self.name, "          ", self.price, "        ", self.avg)

	def printTradeOrder(self, act):
		tz = pytz.timezone('America/New_York') 
		time = datetime.now(tz).strftime("- %H:%M:%S")
		print("\n\n" + act, "order for", self.name, "at",self.price, time)
		print("-------------------------------------------")
		print("Price:", self.price)
		print("1-hour Average:", self.avg)
		print("Z-Score:", round(self.zscore, 2))

	def printTradeSummary(self):
		print(self.name, "     	  ", self.buys, "     ", self.sells)




