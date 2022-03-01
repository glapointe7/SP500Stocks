import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
from tabulate import tabulate

def plot(company, percentage_gains, stock_indices):
    fig, axes = plt.subplots(2, 2, figsize=(25, 20))
    plotPercentageGainPerYear(percentage_gains, company, axes[0, 0])
    plotStockPriceTimeSeries(stock_indices, company, axes[0, 1])
    plotStockPriceTimeSeries(stock_indices, company, axes[1, 0], last_days = 7)
    axes[1, 1].axis('off')
    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    plt.show()

def plotPercentageGainPerYear(dataset, company, ax):
    company_selected = dataset.loc[dataset['CompanyName'] == company, ['Year', 'PercentageGain']]
    
    ax.bar(company_selected['Year'], company_selected['PercentageGain'])

    ax.set_xlabel('Year', fontdict={'fontsize': 14})
    ax.set_ylabel('Percentage Gain (%)', fontdict={'fontsize': 14})
    ax.set_title('Percentage gain in function of the year', fontdict={'fontsize': 17})

def plotStockPriceTimeSeries(dataset, cie, ax, last_days = 0):
    stocks_company = dataset.loc[dataset['CompanyName'] == cie, 'Date':'Close']
    if last_days > 0:
        stocks_company = stocks_company.tail(last_days)
    stocks_company = stocks_company.set_index('Date')

    stocks_company['Open'].plot(label="Open", ax=ax, legend=True, rot=90)
    stocks_company['Close'].plot(label="Close", ax=ax, legend=True, rot=90)
    stocks_company['High'].plot(label="High", ax=ax, legend=True, rot=90)
    stocks_company['Low'].plot(label="Low", ax=ax, legend=True, rot=90)

    ax.set_xlabel('Date', fontdict={'fontsize': 14})
    ax.set_ylabel('Stock Price ($)', fontdict={'fontsize': 14})
    ax.set_title('Time series of the market stock prices (open, close, high and low)', fontdict={'fontsize': 17})
    
def displayLastDayStockPriceAndGain(dataset, cie):
    stocks_cie = dataset.loc[dataset['CompanyName'] == cie, ['Date', 'Open', 'Close', 'Volume']]
    stocks_cie['PercentageGain'] = (stocks_cie['Close'] - stocks_cie['Open']) / stocks_cie['Open'] * 100
    stocks_cie['Volume'] = stocks_cie['Volume'].astype(np.int64)
    
    open_market_cap = stocks_cie['Open'].iloc[-1] * stocks_cie['Volume'].iloc[-1]
    close_market_cap = stocks_cie['Close'].iloc[-1] * stocks_cie['Volume'].iloc[-1]
    
    last_day_stock_dict = {'Date': [stocks_cie['Date'].iloc[-1]],
                           'Open': [round(stocks_cie['Open'].iloc[-1], 2)],
                           'Close': [round(stocks_cie['Close'].iloc[-1], 2)],
                           'Number of flowing shares': [stocks_cie['Volume'].iloc[-1]],
                           'Percentage gain': [round(stocks_cie['PercentageGain'].iloc[-1], 2)],
                           'Open market cap': [round(open_market_cap, 2)],
                           'Close market cap': [round(close_market_cap, 2)],
                           'Market cap gain': [round(close_market_cap - open_market_cap, 2)]}
    last_day_stock = pd.DataFrame(data=last_day_stock_dict)
    
    print(tabulate(tabular_data=last_day_stock, 
                   showindex=False, 
                   disable_numparse=True, 
                   headers=last_day_stock.columns) + "\n")

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