# Summary
This analysis contains:

- A dashboard of percentage gains and stock price market plots based on a company selected;
- A table of top company gainers or losers based on a period of time selected.

# Dashboard
Based on a company selected in a dropdown list, the dashboard presents:

- The latest open, close, percentage and cap gains of the stock market;
- A plot of the percentage gain in function of the year;
- A time series of the stock market prices from the start (1990-01-01);
- A time series of the stock market prices of the last 7 days.

# Files
The way we created the Python files is to separate the display of information and plots from the data download:

- Dashboard.py contains the preparation of the dataset, display of information asked and plot time series.
- DatasetDownloader.py is used for reading CSV stored on a package yfinance and on https://datahub.io/core/s-and-p-500-companies/ into a data frame that we clean afterwards.
