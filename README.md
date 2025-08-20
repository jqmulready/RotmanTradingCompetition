
# Rotman Trading Competition

This repository contains two algorithmic trading strategies developed and one practice for the Rotman Interactive Trader (RIT) platform. These strategies are designed to operate in simulated trading environments and leverage real-time market data and news feeds to make informed trading decisions.

## Overview

### Strategy 1: Bid-Ask Spread Arbitrage
- Monitors bid and ask prices for a security (e.g., ALGO).
- Submits limit orders when the spread exceeds a predefined threshold.
- Manages open orders and reorders partially filled trades.
- Implements a graceful shutdown mechanism.

### Strategy 2: CAPM Beta-Based Trading
- Parses news articles to extract forward market prices and risk-free rates.
- Calculates expected market returns and security-specific returns.
- Uses CAPM to estimate expected returns for multiple securities.
- Executes market orders based on positive expected returns.

## Repository Structure

```
RotmanTrading-Competition/
│
├── RotmanAlgorithmicArbitrage.py       # Implements bid-ask spread arbitrage strategy
├── RotmanMarketMaking.py         # Implements CAPM beta-based trading strategy
├── RotmanPractice.py         # Original Testing in the RIT environment and playing with differnt options
├── README.md                # Project documentation
```

## Requirements

- Python 3.8 or higher
- Required packages:

```bash
pip install requests pandas matplotlib
```

## Usage

### Running Spread Strategy
1. Set your API key:
```python
API_KEY = {'X-API-Key': 'YOUR_API_KEY'}
```
2. Run the script:
```bash
python spread_strategy.py
```

### Running CAPM Strategy
1. Set your API key:
```python
API_KEY = {'X-API-Key': 'YOUR_API_KEY'}
```
2. Run the script:
```bash
python capm_strategy.py
```

## Methodology

### Spread Strategy
- Trades are executed when the bid-ask spread exceeds a threshold.
- Reorders are triggered if one side of the book is filled and potential profit conditions are met.

### CAPM Strategy
- News parsing extracts forward prices and risk-free rates.
- Historical price data is used to compute returns.
- CAPM formula is applied to estimate expected returns.
- Trades are executed for securities with positive expected returns.

## Notes

- Ensure the RIT client is running locally on port 9999.
- Scripts include safeguards for API errors and graceful shutdown.
- News parsing assumes specific formatting for extracting financial indicators.
