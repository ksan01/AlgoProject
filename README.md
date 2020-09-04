# Simple Mean Reversion Trading Program

*Kerem San* 
<br/><br/>

An automated trading bot that trades a small portfolio of ten stocks using a simple mean reversion trading algorithm.

**Disclaimer:** This program is not a fully developed trading bot that 
promises or attempts to generate positive returns every single trading 
session. The sole purpose of this program is for me to get practice 
translating a simple trading strategy into code and gain experience 
with algorithmic trading.

API: Alpaca Paper Trading API

## The Portfolio
- AAPL (Apple Inc)
- MSFT (Microsoft Corporation)
- FB (Facebook, Inc.)
- TSLA (Tesla Inc)
- GOOG (Alphabet Inc)
- NFLX (Netlix Inc)
- ZM (Zoom Video Communications Inc)
- BRK.B (Berkshire Hathaway Inc)
- JNJ (Johnson & Johnson)
- CVX (Chevron Corporation)

## The Algorithm

For each stock in the portfolio;
- Gets current stock price each minute
- Updates 1-hour moving average of the stock each minute
- Compares current price to moving average by computing z-score.
- If z-score is greater than 1, meaning that the current price is above
  the moving average by at least one standard deviation, executes a SELL order
- If z-score is smaller than -1, meaning that the current price is below
  the moving average by at least one standard deviation, executes a BUY order

Other Features:
- Keeps track of all the buy prices of the stocks so that the algorithm cannot 
wrongfully sell a stock at a lower price than it has been bought
- If the next BUY order will decrease the starting fund by 25%, does not execute
the order or any other BUY orders until the fund increases again, and prints an 
appropriate message
- If the z-score of a stock is greater than 1, but the stock is not in possesion, 
i.e. if there is no stock to sell, does not execute a SELL order and prints an 
appropriate message

## The Program

**Initial screen when the stock market is open prints the portfolio and the starting fund:**
<br/><br/>
<img src="images/open.png" alt="Open" width="50%" height="50%">
<br/><br/>

**When the stock market is closed, prints the message below and exits the program:**
<br/><br/>
<img src="images/closed.png" alt="Closed" width="50%" height="50%">
<br/><br/>

**An example price table that gets printed and updated each minute:**
<br/><br/>
<img src="images/price_table.png" alt="Prices" width="50%" height="50%">
<br/><br/>

**An example BUY order output:**
<br/><br/>
<img src="images/buy.png" alt="BUY" width="50%" height="50%">
<br/><br/>

**An example SELL order output:**
<br/><br/>
<img src="images/sell.png" alt="SELL" width="50%" height="50%">
<br/><br/>

**An example screen that the user views each minute:**
<br/><br/>
<img src="images/screen.png" alt="Screen" width="50%" height="50%">








