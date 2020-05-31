from datetime import datetime
import pytz

class Stock:

	def __init__(self, name):
		self.name   = name
		self.price  = 0
		self.avg    = 0
		self.zscore = 0
		self.count  = 0

	def printPrice(self):
		print(self.name, ":     ", self.price, "              ", self.avg)

	def printTrade(self, act):
		tz = pytz.timezone('America/New_York') 
		time = datetime.now(tz).strftime("%H:%M:%S")
		print("\n", act, "order for", self.name, "at",self.price, time)
		print("Price: ", self.price)
		print("1-hour Average: ", self.avg)
		print("Z-Score: ", self.zscore)

