import bs4
from bs4 import BeautifulSoup
import sys 
from urllib.request import Request, urlopen
import requests
import pandas as pd
from functools import reduce


def get_html(url):
    headers = requests.utils.default_headers()
    headers.update(
        {"User-Agent":"Mozilla/5.0"}
    )
    page = requests.get(url,headers=headers)
    data = BeautifulSoup(page.content,'html.parser')
    return data


def get_tags(data):
    products_ = []
    prices = []

    try:
        product_id    = data.find_all('div',attrs={'class':'product_name'})
        offer_price   = data.find_all('span', attrs={'price'})

        for products in product_id:
            prod_clean = products.text.strip('\n')
            products_.append(prod_clean)
        
        for data in offer_price:
            elems = repr(data.text)
            for elems in data:
                prices.append(elems.translate({ord(i): None for i in '\n\t\t\t'}))
    
        return convert(products_,prices)
    except:
        print(sys.exc_info()[0], sys.exc_info()[1])


def convert(products_,prices):
    items_map = {
        'Product' : {i: products_[i] for i in range(1,len(products_))},
        'Price'   : {i: prices[i] for i in range(len(prices))},
        }
    return items_map

def table(items_map):
    data = pd.DataFrame().from_dict(data=items_map,orient='columns')
    prod_data  = data.iloc[1:,0]
    price_data = data.iloc[:,1].shift(1)
    result = pd.concat([prod_data,price_data],axis=1)
    beers = result.drop([0],axis=0)
    return beers.dropna()

def retrieve_promos(url):
    data               = get_html(url)
    items_map          = get_tags(data)
    items_table        = table(items_map)
    return items_table


# if __name__ == "__main__":
#     url  = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16'
#     url2 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15'
#     url2 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15'
#     url3 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16/lager-16023'
#     url4 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/coolers-18-1'
#     url5 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16/hybrid-16024'
#     url6 = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16/lager-16023/flavoured-beer-16023306-1'
#     url_list = [url,url2,url3]
#     for urls in url_list:
#         items = retrieve_promos(urls)
#         print(items)
 
    
