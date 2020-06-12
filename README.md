# Simple Mean Reversion Trading Program

Kerem San



An automated trading bot using a simple mean reversion trading strategy.

## The Algorithm

- Gets current stock price each minute
- Updates 1-hour moving average of stock each minute
- Compares current price to moving average by computing z-score.
- If z-score is greater than 1, meaning that the current price is above
  the moving average by at least one standard deviation, executes a SELL order
- If z-score is smaller than -1, meaning that the current price is below
  the moving average by at least one standard deviation, executes a BUY order