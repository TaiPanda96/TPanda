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

class Valuation:
    def __init__(self,url_head,filename):
        self.url_head = url_head
        self.filename = filename
        self.file = None 

    def file_constructor(self):
        path = '/Users/taishanlin/Desktop/Python Files/'
        self.file = path + self.filename
        return self.file 

    def get_companies(self):
        companies = []
        data_set = pd.read_excel(self.file)
        for i in data_set['ID']:
            companies.append(i)
        return companies

    def get_symbol(self):
        data = pd.read_excel(self.file)
        query_strings = {
            'url_analysis'    : self.url_head + data['ID'] + '/analysis?p='   +  data['ID'],
            'url_options'     : self.url_head + data['ID'] + '/options?p='    +  data['ID'],
            'url_cashflow'    : self.url_head + data['ID'] + '/cash-flow?p='  +  data['ID'],
            'url_financials'  : self.url_head + data['ID'] + '/financials?p=' +  data['ID'],
        }
        url_table = pd.DataFrame.from_dict(query_strings,orient='columns')
        url_table.to_excel('/Users/taishanlin/Desktop/Django Documentation/URL_Query_Output.xlsx')
        return url_table

def get_soup(url_table):
    symbols = symbol_list()
    j = 0
    while j <= len(symbols):
        for url in url_table:
                EPS = []
                EPS_data = []
                EPS_data_2 = []
                EPS_data_3 = []
                EPS_data_4 = []
                try:
                    response = requests.get(url)
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
                                                    'Earnings':     EPS,
                                                    'Current Qtr':  EPS_data,
                                                    'Next Qtr':     EPS_data_2,
                                                    'Current Year': EPS_data_3,
                                                    'Next Year':    EPS_data_4,}
                    table = pd.DataFrame.from_dict(dict(itertools.islice(dic_ob.items(),len(dic_ob))))
                    table.to_csv('/Users/taishanlin/Desktop/Django Documentation/Earnings Table/' + symbols[j] + '.csv')
                    print('{}'.format(symbols[j]),'Successful')
                    j += 1 
                except:
                    break
    print('Task Complete')
      

#static method
def symbol_list():
    excel = '/Users/taishanlin/Desktop/Python Files/SP500_Master_Combined.xlsx'
    df = pd.read_excel(excel)
    company_ticker = list(df['ID'])
    return company_ticker


if __name__ == "__main__":
    test = Valuation("https://ca.finance.yahoo.com/quote/","SP500_Master_Combined.xlsx")
    x = test.file_constructor()
    y = test.get_symbol()
    url_table = list(y['url_analysis'])
    get_soup(url_table)