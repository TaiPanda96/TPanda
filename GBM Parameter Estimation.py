#%%
import seaborn as sns
import math
import numpy as np
from datetime import datetime
import pandas as pd 
from DataEngine import Data_Engine

def scatter_plot(csv):
    dataset = pd.read_csv(csv)
    #graph1 = sns.scatterplot(x="Date",y="Adj Close",data=dataset)
    graph2 = sns.scatterplot(x="Open",y="Adj Close",data=dataset)
    return graph2 

def correlation_matrix(csv):
    dataset = pd.read_csv(csv)
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

def scatter(csv):
    data = log_returns_timeseries(csv)
    graph = sns.scatterplot(x='Date',y='Log Returns',data=data)
    return graph

if __name__ == "__main__":
    csv = '/Users/taishanlin/Desktop/Python Files/ZTS.csv'
    #scatter_plot(csv)
    #log_return_plot(csv)
    #correlation_matrix(csv)
    #correlation_matrix(csv)
    log_returns_timeseries(csv)
    # scatter(csv)
    # #print(log_return(csv))
