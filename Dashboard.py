import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

def plotPercentageGainPerYear(dataset, cie):
    cie_selected = dataset.loc[dataset['CompanyName'] == cie, ['Year', 'PercentageGain']]
    
    plt.figure(figsize=(20, 10))
    plt.bar(cie_selected['Year'], cie_selected['PercentageGain'])

    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Percentage Gain (%)', fontsize=16)
    plt.title("Percentage gain in function of the year", fontsize=20)

    plt.show()

def plotStockPriceTimeSeries(dataset, cie, last_days = 0):
    stocks_company = dataset.loc[dataset['CompanyName'] == cie, 'Date':'Close']
    if last_days > 0:
        stocks_company = stocks_company.tail(last_days)
    stocks_company = stocks_company.set_index('Date')

    plt.figure(figsize=(25, 10))
    stocks_company['Open'].plot(label="Open")
    stocks_company['Close'].plot(label="Close")
    stocks_company['High'].plot(label="High")
    stocks_company['Low'].plot(label="Low")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stock Price ($)', fontsize=16)
    plt.title("Time series of the market stock prices (open, close, high and low)", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)

    plt.legend()
    plt.show()
    

def displayLastDayStockPriceAndGain(dataset, cie):
    stocks_cie = dataset.loc[dataset['CompanyName'] == cie, ['Date', 'Open', 'Close', 'Volume']]
    stocks_cie['PercentageGain'] = (stocks_cie['Close'] - stocks_cie['Open']) / stocks_cie['Open'] * 100
    stocks_cie['Volume'] = stocks_cie['Volume'].astype(np.int64)
    
    open_market_cap = stocks_cie['Open'].iloc[-1] * stocks_cie['Volume'].iloc[-1]
    close_market_cap = stocks_cie['Close'].iloc[-1] * stocks_cie['Volume'].iloc[-1]
    
    print("\n---------------------------------------------------")
    print("Date: {:%Y-%m-%d}".format(stocks_cie['Date'].iloc[-1]))
    print("\nOpen: {:.6f} $/share".format(stocks_cie['Open'].iloc[-1]))
    print("\nClose: {:.6f} $/share".format(stocks_cie['Close'].iloc[-1]))
    print("\nNumber of flowing shares: {:d}".format(stocks_cie['Volume'].iloc[-1]))
    print("\nPercentage gain: {:.2f} %".format(stocks_cie['PercentageGain'].iloc[-1]))
    print("\nOpen market cap: {:.2f} $".format(open_market_cap))
    print("\nClose market cap: {:.2f} $".format(close_market_cap))
    print("\nMarket cap gain: {:.2f} $".format(close_market_cap - open_market_cap))
    print("---------------------------------------------------\n")

def showBiggestCiesGainerOverTime(dataset, from_date):
    stocks = dataset.loc[dataset['Date'] > from_date, ['CompanyName' ,'Open', 'Close']]

    stocks = stocks.groupby(['CompanyName']) \
                   .agg(Open=pd.NamedAgg(column="Open", aggfunc="first"), 
                        Close=pd.NamedAgg(column="Close", aggfunc="last")) \
                   .reset_index()
    stocks['PercentageGain'] = (stocks['Close'] - stocks['Open']) / stocks['Open'] * 100
    stocks.loc[stocks['PercentageGain'] == np.inf, 'PercentageGain'] = 0.0
    stocks = stocks.sort_values(by="PercentageGain", ascending=False)

    print("From: {:%Y-%m-%d}".format(from_date))
    display(stocks)