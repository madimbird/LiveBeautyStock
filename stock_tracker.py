"""
Beauty Stock Tracker App - Main Module

Author: Madeline Martin-Bird
Github: https://github.com/madimbird
Date: September 2023
Version: 1

##Purpose: This app allows users to track stock prices of popular beauty stocks

Dependencies:

Usage:


License: [Specify the License, e.g., MIT License]
"""
from flask import Flask, render_template
from decouple import config
import requests
import json
import time


app=Flask(__name__)

API_KEY=config('API_KEY')
stock_symbols = ['ELF', 'OLPX', 'ULTA']  # List of stocks to track
stock_data = {symbol: {'symbol': symbol, 'price': None, 'timestamp': None} for symbol in stock_symbols}


@app.route('/')
def index():
    return render_template('index.html', stock_symbols=stock_symbols, stock_data=stock_data)

def fetch_stock_price(symbol):
    while True:
        try:
            #Alpha Vantage API endpoint for stock price
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'

            response = requests.get(url)
            data = json.loads(response.text)

            if 'Time Series (1min)' in data:
                #get latest stock price
                latest_data = list(data['Time Series (1min)'].values())[0]
                stock_data[symbol] ={
                    'symbol' : symbol,
                    'price' : latest_data['1. open'],
                    'timestamp' : data['Meta Data']['3. Last Refreshed']
                }

        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")

        time.sleep(60) #fetch data every 60 seconds

if __name__ == '__main__':
    # Start the data fetching process in a separate thread
    from threading import Thread

    for symbol in stock_symbols:
        data_thread = Thread(target=fetch_stock_price, args=(symbol,))
        data_thread.daemon = True
        data_thread.start()

    app.run(debug=True)