## Import Libraries Used
import pandas as pd 
import numpy as np
import lxml as lxml
from lxml import objectify
from lxml import html
from time import sleep
import xlsxwriter as xlsx
import itertools

# Classes Used from Another File
from DataEngine import Data_Engine
import xml.etree.ElementTree as etree

# Scraping Libraries Used
import time, requests, lxml
from collections import OrderedDict
from bs4 import BeautifulSoup


def income_soup(url):
    response = requests.get(url)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data,features='lxml')

    Income_Statement = []
    Income_Data = []

    for div_class in soup.find_all('div',class_='D(ib)'):
        Income_Statement.append(div_class.text)

        dict_financials = {
        'Fields': Income_Statement[11:17],}
    
    for div_class in soup.find_all('div',class_='D(tbc)'):
        Income_Data.append(div_class.text)
        data = {
            'TotalRevenue'                                       : Income_Data[0:6],
            'Cost of Revenue'                                    : Income_Data[6:12],
            'Gross Profit'                                       : Income_Data[12:18],
            'Operating Expenses'                                 : Income_Data[18:24],
            'Research Development'                               : Income_Data[24:30],
            'SGA'                                                : Income_Data[30:36],
            'Operating Expense'                                  : Income_Data[36:42],
            'Operating Income or Loss'                           : Income_Data[42:48],
            'Interest Expense'                                   : Income_Data[48:54],
            'Total Other Income or ExpenseNet'                   : Income_Data[54:60],
            'Income Before Tax'                                  : Income_Data[60:66],
            'Income Tax Expense'                                 : Income_Data[66:72],
            'Income from Continuing Operations'                  : Income_Data[72:78],
            'Net Income'                                         : Income_Data[78:84],
            'Net Income Available to Common Stock Shareholders'  : Income_Data[84:90],
            'EBITDA'                                             : Income_Data[90:96],
        }

    rows_to_drop = [0,1,3,4,5,7,8,9,10,32,33,34]

    ## Income Fields
    df = pd.DataFrame.from_dict(dict_financials,orient='columns')
    
    ## Income Data
    table = pd.DataFrame.from_dict(data,orient='columns')
    final_table = table.drop(rows_to_drop[0])

    ## Building the Income Table
    income_table = pd.concat([df.shift(1),final_table],axis=1)
    new_income_table = income_table.drop(income_table.index[0])
    income_table.to_csv('/Users/taishanlin/Desktop/Django Documentation/Income_Table.csv')
    return new_income_table

if __name__ == "__main__":
    url = 'https://ca.finance.yahoo.com/quote/MMM/financials?p=MMM'
    test_table = income_soup(url)
    print(test_table)
    