#%%
import seaborn as sns
import math
import numpy as np
from datetime import datetime
import pandas as pd 
from DataEngine import Data_Engine

def rate_of_change(csv):
    dataset = pd.read_csv(csv)
    volume = dataset['Volume']
    price_lag = dataset['Open'].shift(1)
    volume_lag = dataset['Volume'].shift(1)
    price = dataset['Open']
    change = price - price_lag
    change_percent = change/price_lag
    change_vol = volume - volume_lag
    change_vol_percent = change_vol/volume_lag
    
    data = {
        'date': dataset['Date'],
        'price0': price_lag,
        'price_chg': change,
        'price': dataset['Open'],
        'close_price': dataset['Adj Close'],
        'volume0': volume_lag,
        'volume': dataset['Volume'],
        'price_chg_%': change_percent,
        'volume_chg': change_vol,
        'volume_chg_%': change_vol_percent,
        'diff': dataset['Adj Close'] - dataset['Open'],
    }
    cols = [i for i in data]
    
    df = pd.DataFrame(data,columns=cols)
    return df 

def scatter_plot(csv):
    data = rate_of_change(csv)
    graph = sns.scatterplot(x="price",y="close_price",hue="close_price",data=data)
    #graph2 = sns.scatterplot(x="Open",y="Adj Close",data=dataset)
    return graph

def correlation_matrix(csv):
    dataset = rate_of_change(csv)
    corr_matrix = dataset.corr()
    heat_map = sns.heatmap(corr_matrix,annot=True)
    return heat_map 


def log_return(csv):
    dataset = pd.read_csv(csv)
    open_price  = dataset['Open']
    close_price = dataset['Adj Close']
    total_daily_return = close_price/open_price
    log_total_daily_return = np.log(total_daily_return)
    return log_total_daily_return

def log_return_plot(csv):
    dataset = pd.read_csv(csv)
    data = {   
        'Daily Log Return':  log_return(csv),
        'Volume':  np.log(dataset['Volume']),
                }
    df = pd.DataFrame(data,columns=['Daily Log Return','Volume'])
    graph = sns.scatterplot(x="Daily Log Return",y="Volume",data=df)
    # lineplot = sns.lineplot(x="Daily Log Return",y="Volume",data=data)
    return graph


def log_returns_timeseries(csv):
    data_set = pd.read_csv(csv)
    date = data_set['Date']
    returns = log_return(csv)
    df_log_return = pd.DataFrame(returns,columns=['Log Returns'])
    returns_table = pd.concat([date,df_log_return],axis=1)
    df = pd.DataFrame(data=returns_table,columns=['Date','Log Returns'])
    graph = sns.scatterplot(x="Date",y="Log Returns",data=df)
    return graph


def line_plot2(csv):
    data = pd.read_csv(csv)
    lineplot_adjclose = sns.lineplot(x="Date",y="Adj Close",data=data)
    #lineplot_open = sns.lineplot(x="Date",y="Open",data=data)
    #lineplot_high_low = sns.lineplot(x="Date",y="Volume",data=data)
    return lineplot_adjclose

if __name__ == "__main__":
    csv = '/Users/taishanlin/Desktop/Python Files/ZTS.csv'
    print(rate_of_change(csv))
    #scatter_plot(csv)
    #correlation_matrix(csv)
    #log_return_plot(csv)
