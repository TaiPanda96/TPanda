import pandas as pd 
import numpy as np
import lxml as lxml
from lxml import objectify
from lxml import html
from time import sleep
import xlsxwriter as xlsx
import itertools

from DataEngine import Data_Engine
import xml.etree.ElementTree as etree

import time, requests, lxml
from collections import OrderedDict
from bs4 import BeautifulSoup

class Valuation:
    def __init__(self,url_head, url_tail,filename):
        self.url_head = url_head
        self.url_tail = url_tail
        self.filename = filename
        self.file = None 

    def file_constructor(self):
        path = '/Users/taishanlin/Desktop/Python Files/'
        self.file = path + self.filename
        return self.file 

    def get_symbol(self):
        data = pd.read_excel(self.file)
        url = self.url_head + data['ID'] + self.url_tail + data['ID']
        return url

    def get_companies(self):
        companies = []
        data_set = pd.read_excel(self.file)
        for i in data_set['ID']:
            companies.append(i)
        return companies

class Run:
    def __init__(self):
        self.options    = Valuation('https://ca.finance.yahoo.com/quote/','options?p=','SP500_Master_Combined.xlsx')
        self.financials = Valuation('https://ca.finance.yahoo.com/quote/','financials?p=','SP500_Master_Combined.xlsx')
        self.cash_flow  = Valuation('https://ca.finance.yahoo.com/quote/','cash-flow?p=','SP500_Master_Combined.xlsx')
        self.analysis   = Valuation('https://ca.finance.yahoo.com/quote/','analysis?p=','SP500_Master_Combined.xlsx')
    
    def construct(self):
        self.options.file_constructor()
        self.financials.file_constructor()
        self.cash_flow.file_constructor()
        self.analysis.file_constructor()

    def run(self):
        A = list(self.options.get_symbol())
        B = list(self.financials.get_symbol())
        C = list(self.cash_flow.get_symbol())
        D = list(self.analysis.get_symbol())
        dict_db = {
            'A': A,
            'B': B,
            'C': C,
            'D': D,}
        return pd.DataFrame.from_dict(dict_db, orient='columns')

def get_soup(url):
    EPS = []
    EPS_data = []
    EPS_data_2 = []
    EPS_data_3 = []
    EPS_data_4 = []
    try:
        website_request(url)
        response = website_request(url)
        for url in response:
            data = response.text
            soup = BeautifulSoup(data,features='lxml')
            for tr in soup.find_all('tr', attrs={'class':'BdT Bdc($seperatorColor)'}):
                for td in tr.find_all('td',attrs={'class':'Py(10px) Ta(start)'}):
                    for span in td.find_all('span'):
                        EPS.append(span.text)
                        for col1 in span.find_next('span'):
                            EPS_data.append(col1)
                            for col2 in col1.find_next('span'):
                                EPS_data_2.append(col2)
                                for col3 in col2.find_next('span'):
                                    EPS_data_3.append(col3)
                                    for col4 in col3.find_next('span'):
                                        EPS_data_4.append(col4)
                dic_ob = {
                    'Earnings': pd.Series(EPS),
                    'Current Qtr': pd.Series(EPS_data),
                    'Next Qtr': pd.Series(EPS_data_2),
                    'Current Year': pd.Series(EPS_data_3),
                    'Next Year': pd.Series(EPS_data_4),
                        }
                table = pd.DataFrame.from_dict(dict(itertools.islice(dic_ob.items(),5)))
            return table
    except:
        print('Error in Request')
    

def get_earnings_table(Run):
    allEarnings = pd.DataFrame()
    raw_table = Run.run()
    data = raw_table['D']
    symbol_list = list(Data_Engine.get_symbol_list)
    idx = 0
    if idx > len(data):
        print('There is no data for this company')
    else:
        while idx <= len(data['D']):
            for url in data['D']:
                earnings_data = get_soup(url)
                for j in symbol_list:
                    earnings_data.to_csv("/Users/taishanlin/Desktop/Python Files/Earnings Table/" + j + ".csv")
                    allEarnings.append(earnings_data,ignore_index=True)
    return allEarnings

                

if __name__ == "__main__":
    # Below code 
    obj1 = Run()
    x = obj1.construct
    print(x())
    y = obj1.run
    print(y())
    #url = 'https://ca.finance.yahoo.com/quote/ABBV/analysis?p=ABBV'

   