from neuralintents import BasicAssistant, GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
from pandas_datareader import data as pdr
import yfinance as yfin
import mplfinance as mpf
import pickle
import sys
import datetime as dt

yfin.pdr_override()

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

def save_portfolio():
    with open('portfolio.pkl','wb') as f:
        pickle.dump(portfolio,f)

def add_portfolio():
    ticker = input("Which stock do you want to add : ")
    amount = input("How many shares do you want to add :")
    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)
    save_portfolio()

def remove_portfolio():
    ticker = input("Which stock do you want to sell : ")
    amount = input("How many shares do you want to sell : ")
    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
            save_portfolio()
        else:
            print("You don't have enough shares!")
    else:
        print(f"You don't own any shares of {ticker}")

def show_portfolio():
    print("Your portfolio : ")
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")

def portfolio_worth():
    sum=0
    for ticker in portfolio.keys():
        #data = web.DataReader(ticker, 'yahoo')
        data = pdr.get_data_yahoo(ticker)
        price = data['Close'].iloc[-1]
        sum += price
    print(f"Your portfolio is worth {sum} USD")

def portfolio_gains():
    starting_date = input("Enter a date for comparison (YYYY-MM-DD) : ")
    sum_now=0
    sum_then=0
    try:
        for ticker in portfolio.keys():
            #data = web.DataReader(ticker, 'yahoo')
            data = pdr.get_data_yahoo(ticker)
            price_now = data['Close'].iloc[-1]
            price_then = data.iloc[data.index==starting_date]['Close'].values[0]
            sum_now+=price_now
            sum_then+=price_then
        print(f"Relative Gains : {((sum_now-sum_then)/sum_then)*100}%")
        print(f"Absolute Gains : {sum_now-sum_then} USD")
    except IndexError:
        print("There was no trading on this day!")

def plot_chart():
    ticker = input("Choose a ticker symbol : ")
    starting_string = input("Choose a starting date (DD/MM/YYYY) : ")
    plt.style.use('dark_background')
    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()
    #data = web.DataReader(ticker, 'yahoo', start, end)
    data = pdr.get_data_yahoo(ticker, start, end)
    colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    mpf.plot(data, type='candle', style=mpf_style, volume=True)


def bye():
    print("Goodbye!")
    sys.exit(0)

def greeting():
    print("Hello!")

mappings = {
    'greeting' : greeting,
    'plot_chart': plot_chart,
    'add_portfolio' : add_portfolio,
    'remove_portfolio' : remove_portfolio,
    'show_portfolio' : show_portfolio,
    'portfolio_worth' : portfolio_worth,
    'portfolio_gains' : portfolio_gains,
    'bye' : bye
}


assistant = BasicAssistant('intents.json', mappings, "Financial AI-Assistant")
#assistant.fit_model()
#assistant.save_model()
assistant.load_model()
while True:
    message = input("")
    assistant.process_input(message)
