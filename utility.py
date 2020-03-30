import datetime as dt 
import pandas as pd
import pandas_datareader.data as web
import plotly.graph_objects as go

# Call to the Yahoo Finance API to get stock data
# Returns a dataframe including date, open, close, high, low, and adjusted low prices for a specific stock
# Input --> the stock ticker abbreviation desired
def getStockDataFiveYr(ticker):
    data = web.get_data_yahoo(ticker, start = '2015-01-01', end = dt.datetime.now())
    df = pd.DataFrame(data)
    return df

def getStockDataYr(ticker):
    data = web.get_data_yahoo(ticker, start = '2019-01-01', end = dt.datetime.now())
    df_raw = pd.DataFrame(data)
    df = df_raw.reset_index()
    return df


