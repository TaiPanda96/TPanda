#%%
import seaborn as sns; sns.set()
import math
import numpy as np
from datetime import datetime
import pandas as pd 
import matplotlib.pyplot as plt
from DataEngine import Data_Engine

def scatter_plot(csv):
    dataset = pd.read_csv(csv)
    graph = sns.scatterplot(x="Date",y="Adj Close",data=dataset)
    return graph

def log_return(csv):
    dataset = pd.read_csv(csv)
    open_price  = dataset['Open']
    close_price = dataset['Adj Close']
    total_daily_return = close_price/open_price
    log_total_daily_return = np.log10(total_daily_return)
return log_total_daily_return

def get_symbol_list(excel):
    symbol_list = []
    data = pd.read_excel(excel)
    for i in data['ID']:
        symbol_list.append(i)
        for j in symbol_list:
            csv = '/Users/taishanlin/Desktop/Python Files/{}.csv'.format(j)
    return csv



    
if __name__ == "__main__":
    csv = '/Users/taishanlin/Desktop/Python Files/ZTS.csv'
    #scatter_plot(csv)
    print(log_return(csv))
    # tips = sns.load_dataset("tips")
    # ax = sns.scatterplot(x="total_bill", y="tip", data=tips)
    # ax = sns.scatterplot(x="total_bill", y="tip", hue="time",data=tips)
    # ax = sns.scatterplot(x="total_bill", y="tip",hue="day", style="time", data=tips)
