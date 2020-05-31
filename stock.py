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
		print(self.name, ":     " + str(self.price), "              ",
			 str(self.avg))

	def printTrade(self, act):
		print("\n" + act + " order for " + self.name + " at " + str(self.price))
		tz = pytz.timezone('America/New_York') 
		time = datetime.now(tz).strftime("%H:%M:%S")
		print(", " + time)
		print("\nPrice: " + str(self.price))
		print("\n1-hour Average: " + str(self.avg))
		print("\nZ-Score: " + str(self.zscore) + "\n")

