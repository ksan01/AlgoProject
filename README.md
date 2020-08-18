# Simple Mean Reversion Trading Program

*Kerem San* 
<br/><br/>

An automated trading bot that trades a small portfolio of five stocks using a simple mean reversion trading algorithm.

**Disclaimer:** This program is not a fully developed trading bot that 
promises or attempts to generate positive returns every single trading 
session. The sole purpose of this program is for me to get practice 
translating a simple trading strategy into code and gain experience 
with algorithmic trading.

## The Portfolio
- 2 Technology stocks: AAPL (Apple Inc), MSFT (Microsoft Corporation)
- 1 Consumer Staples stock: WMT (Walmart Inc)
- 1 Healthcare stock: JNJ (Johnson & Johnson)
- 1 Energy stock: CVX (Chevron Corporation)

## The Algorithm

For each stock in the portfolio;
- Gets current stock price each minute
- Updates 1-hour moving average of the stock each minute
- Compares current price to moving average by computing z-score.
- If z-score is greater than 1, meaning that the current price is above
  the moving average by at least one standard deviation, executes a SELL order
- If z-score is smaller than -1, meaning that the current price is below
  the moving average by at least one standard deviation, executes a BUY order

## The Program

**Initial screen when the stock market is open prints the portfolio and the starting fund:**
<br/><br/>
![Open](images/open.png)<!-- .element height="50%" width="50%" -->
<br/><br/>

**When the stock market is closed, prints the message below and exits the program:**
<br/><br/>
![Closed](images/closed.png)
<br/><br/>

**The price table below gets printed and updated each minute:**
<br/><br/>
![Prices](images/price_table.png)
<br/><br/>

**An example BUY order output:**
<br/><br/>
![BUY](images/buy.png) 
<br/><br/>

**An example SELL order output:**
<br/><br/>
![SELL](images/sell.png) 
<br/><br/>

**An example screen that the user views each minute:**
<br/><br/>
![Screen](images/screen.png)






