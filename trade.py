import alpaca_trade_api as tradeapi

api = tradeapi.REST()


def checkMarket():
	clock = api.get_clock()
	return clock.is_open

def main():

	if (not checkMarket()):
		print("\nMarket is currently closed, exiting.\n")
		exit()
		
	print("\nMarket is currently open\n")

	while (checkMarket()):
		print("\nMarket Open\n")
		sleep(60)

if __name__ == '__main__':
	main()