# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 20:32:25 2024

@author: anind
"""

import signal
import requests
from time import sleep
import pandas as pd

# Exception class for API errors
class ApiException(Exception):
    pass

# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

# API key and session setup
API_KEY = {'X-API-Key': 'L80RANA5'}
shutdown = False
session = requests.Session()
session.headers.update(API_KEY)

# Function to get current tick from the API
def get_tick(session):
    resp = session.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['tick']
    raise ApiException('fail - cant get tick')

# Function to get news and calculate CAPM values
def get_news(session):
    news = session.get('http://localhost:9999/v1/news')
    if news.ok:
        newsbook = news.json()
        for i in range(len(newsbook[-1]['body'])):
            if newsbook[-1]['body'][i] == '%':
                CAPM_vals['%Rf'] = round(float(newsbook[-1]['body'][i - 4:i])/100, 4)
        latest_news = newsbook[0]
        if len(newsbook) > 1:
            for j in range(len(latest_news['body']) - 1, 1, -1):
                while latest_news['body'][j] != '$':
                    j -= 1
            CAPM_vals['forward'] = float(latest_news['body'][j + 1:-1])
        return CAPM_vals
    raise ApiException('timeout')

# Function to populate prices for securities
def pop_prices(session):
    price_act = session.get('http://localhost:9999/v1/securities')
    if price_act.ok:
        prices = price_act.json()
        return prices
    raise ApiException('fail - cant get securities')

# Function to decide buying or selling based on expected returns
def buy_or_sell(session, expected_return):
    for ticker, exp_return in expected_return.items():
        if exp_return > .0005:
            session.post('http://localhost:9999/v1/orders', params={'ticker': ticker, 'type': 'MARKET', 'quantity': 100, 'action': 'BUY'})
        elif exp_return <= .0005:
            session.post('http://localhost:9999/v1/orders', params={'ticker': ticker, 'type': 'MARKET', 'quantity': 100, 'action': 'SELL'})

# Main function to execute the trading strategy
def main():
    global session  # Use the global session object
    CAPM_vals = {'%Rf': 0.0, 'forward': 0.0}  # Initial values for CAPM_vals
    expected_return = {}
    ritm = pd.DataFrame(columns=['RITM', 'BID', 'ASK', 'LAST', '%Rm'])
    alpha = pd.DataFrame(columns=['ALPHA', 'BID', 'ASK', 'LAST', '%Ri', '%Rm'])
    gamma = pd.DataFrame(columns=['GAMMA', 'BID', 'ASK', 'LAST', '%Ri', '%Rm'])
    theta = pd.DataFrame(columns=['THETA', 'BID', 'ASK', 'LAST', '%Ri', '%Rm'])

    while not shutdown:
        current_tick = get_tick(session)
        if current_tick >= 600:
            break

        # Initialize CAPM_vals before updating it
        CAPM_vals = {'%Rf': 0.0, 'forward': 0.0}
        
        # Fetch news and update CAPM_vals
        try:
            CAPM_vals = get_news(session)
        except ApiException as e:
            print(f"API error occurred while fetching news: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while fetching news: {e}")

        try:
            prices = pop_prices(session)
            # Check if prices is a list
            if isinstance(prices, list):
                print("Received unexpected data format for prices. Expected dictionary.")
                continue
        except ApiException as e:
            print(f"API error occurred while fetching prices: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while fetching prices: {e}")
            continue
        
        # Update ritm, alpha, gamma, theta DataFrames with new prices
        for security, price_info in prices.items():
            if security.startswith('RITM'):
                ritm.loc[len(ritm)] = [security] + [price_info[key] for key in ['bid', 'ask', 'last']]
            elif security.startswith('ALPHA'):
                alpha.loc[len(alpha)] = [security] + [price_info[key] for key in ['bid', 'ask', 'last']]
            elif security.startswith('GAMMA'):
                gamma.loc[len(gamma)] = [security] + [price_info[key] for key in ['bid', 'ask', 'last']]
            elif security.startswith('THETA'):
                theta.loc[len(theta)] = [security] + [price_info[key] for key in ['bid', 'ask', 'last']]
        
        # Calculate beta values and expected returns for ALPHA, GAMMA, THETA
        # Note: You need to implement these calculations based on your strategy
        
        # Example placeholder for buy_or_sell logic
        # Adjust with real expected return calculations
        expected_return = {'ALPHA': 0.001, 'GAMMA': 0.002, 'THETA': 0.0015}
        buy_or_sell(session, expected_return)

        print(expected_return)
        sleep(1)  # Sleep to rate limit our loop (adjust as needed)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        main()
    except ApiException as e:
        print(f"API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
