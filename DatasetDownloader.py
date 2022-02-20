## Source: https://datahub.io/core/s-and-p-500-companies#python
import Utils
import pandas as pd

Utils.installPackageIfNotInstalled("datapackage")
from datapackage import Package

def downloadCompanyBasicInformation():
    package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')

    # Store list of lists of 3 strings from the JSON file: 
    # Company abbreviation, company name and sector of activities.
    companies = list()
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            companies = resource.read()
    
    return companies

Utils.installPackageIfNotInstalled("yfinance")
import yfinance as yf

def downloadStockIndicesToCSVFile(companies):
    dataset_list = list()
    for company in companies:
        data = yf.download(tickers=company, 
                        group_by="Ticker", 
                        start='1989-12-31', 
                        progress=False)
        data['CompanyAbbreviation'] = company 
        dataset_list.append(data)

    # combine all dataframes into a single dataframe
    return pd.concat(dataset_list)
