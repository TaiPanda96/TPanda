import pandas as pd 
from pandas_datareader import data,wb
from pandas_datareader import data as web
import datetime


class Data_Engine:
    def __init__(self, symbol_list, s_year, s_month, s_day, e_year, e_month, e_day):
        self.symbol_list = None
        self.s_year = s_year
        self.s_month = s_month 
        self.s_day = s_day
        self.e_year = e_year
        self.e_month = e_month 
        self.e_day = e_day
    
    def get_symbol_list(self, excel):
        self.symbol_list = []
        data = pd.read_excel(excel)
        for i in data['ID']:
            self.symbol_list.append(i)
        return self.symbol_list

    def get_stock(self, symbol_list):
        symbol_list = self.symbol_list
        start = datetime.datetime(self.s_year,self.s_month,self.s_day)
        end = datetime.datetime(self.e_year,self.e_month,self.e_day)
        for i in symbol_list:
            if i is not None: 
                try:
                    df = web.DataReader(i,'yahoo',start,end)
                    print("{}".format(i),"FETCH SUCCESSFUL")
                except:
                    print("{}".format(i),"Caught an Exception: Company Does Not Exist on Yahoo Finance")
                    continue
        print("Fetch is Complete")
        return df 

    def __str__(self):
        return 'Symbol is={},Start Year is {}, End Year is {}'.format(self.symbol_list,self.s_year,self.e_year)
    
if __name__ == "__main__":
    excel = "/Users/taishanlin/Desktop/Python Files/SP500_Master_Combined.xlsx"
    objA = Data_Engine([],2000,1,1,2020,2,22)
    result = objA.get_stock(objA.get_symbol_list(excel))
    print(result)