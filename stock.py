
class Stock:

	def __init__(self, name):
		self.name   = name
		self.price  = 0
		self.avg    = 0
		self.zscore = 0
		self.count  = 0

	def printPrice(self):
		print(self.name + ": " + str(self.price) + "\n")

	def printTrade(self, act):
		print("\n" + act + " order for " + self.name + " at " + str(self.price))
		print("\nPrice: " + str(self.price))
		print("\n1-hour average: " + str(self.avg))
		print("\nZ-Score: " + str(self.zscore) + "\n")

