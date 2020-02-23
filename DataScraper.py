#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:20:08 2019

@author: taishanlin
"""
import pandas as pd
import lxml
from lxml import html
import requests
import urllib3 
import xlsxwriter as xl
from bs4 import BeautifulSoup


def data_engine(symbol_list):
    url_head = "https://ca.finance.yahoo.com/quote/"
    url_tail = "/history?p="
    Date = [] 
    Elements = []
    High = []
    Low = [] 
    Close = []
    Adj_Close = [] 
    Volume = []
    for symbol in symbol_list:
        url = url_head + symbol + url_tail + symbol
        print('URL Result is',url)
        request = requests.get(url)
        data = request.text
        soup = BeautifulSoup(data,features='lxml')
        
        for tr in soup.find_all('tr', attrs={'class':'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'}):
            for td in tr.find_all('td',attrs={'class':'Py(10px) Ta(start) Pend(10px)'}):
                for span in td.find_all('span'):
                    Date.append(span.text)
                    for open_ in span.find_next('span'):
                        Elements.append(open_)
                        for high in open_.find_next('span'):
                            High.append(high)
                            for low in high.find_next('span'):
                                Low.append(low)
                                for close in low.find_next('span'):
                                    Close.append(close)
                                    for adj_close in close.find_next('span'):
                                        Adj_Close.append(adj_close)
                                        for volume in adj_close.find_next('span'):
                                            Volume.append(volume)
                                        frame = {
                                                'Date':  Date,
                                                'Elements': Elements,
                                                'High':  High,
                                                'Low': Low,
                                                'Close': Close,
                                                'Adj_Close': Adj_Close,
                                                'Volume': Volume
                                                }
                                        result = pd.DataFrame.from_dict(frame, orient='index').transpose()
    return result
    

if __name__ == "__main__":
    symbol_1 = 'BBD-B.TO'
    symbol_2 = 'TSLA'
    symbol_3 = 'UBER'
    symbol_4 = 'UBER.MX'
    symbol_5 = 'ZOOM'
    symbol_list = [symbol_1]
    print(data_engine(symbol_list))

