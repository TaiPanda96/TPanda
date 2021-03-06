# Key Data Structure Libraries
import pandas as pd
import numpy as np

# Key Functional Libraries
from collections import OrderedDict
from collections import ChainMap
from DataEngine import Data_Engine
import xml.etree.ElementTree as etree
from lxml import objectify

# Key File Converter Library
import xlsxwriter as xlsx

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
        self.eps        = Valuation('https://ca.finance.yahoo.com/quote/','analysis?p=','SP500_Master_Combined.xlsx')
    
    def construct(self):
        self.options.file_constructor()
        self.financials.file_constructor()
        self.cash_flow.file_constructor()
        self.eps.file_constructor()

    def run(self):
        A = list(self.options.get_symbol())
        B = list(self.financials.get_symbol())
        C = list(self.cash_flow.get_symbol())
        D = list(self.eps.get_symbol())
        dict_db = {
            'A': A,
            'B': B,
            'C': C,
            'D': D,}
        return pd.DataFrame.from_dict(dict_db, orient='columns')


if __name__ == "__main__":
    obj1 = Run()
    x = obj1.construct
    print(x())
    y = obj1.run
    print(y())

   
