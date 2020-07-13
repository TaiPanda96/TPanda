import bs4
from bs4 import BeautifulSoup
import sys 
from urllib.request import Request, urlopen
import requests
import pandas as pd

class URL_list:
    def __init__(self,url):
        self.url = []
    
    def create(self,url):
        for url_strings in range(len(url)):
            return self.url.append(url_strings)

    def lcbo_data_response(self,url):
        for url_strings in self.url:
            page_obj = get_tags(url)
        return page_obj


def get_html(url):
    headers = requests.utils.default_headers()
    headers.update(
        {"User-Agent":"Mozilla/5.0"}
    )
    page = requests.get(url,headers=headers)
    return page

def get_tags(url):
    page = get_html(url)
    product_list = []
    prices = []

    if page.status_code == 200:
        data = BeautifulSoup(page.content,'html.parser')
        tag = data.a
        
        # lcbo_id     = data.find_all(attrs={'col-xs-7 product_info product-info-section'})
        product_id  = data.find_all('div',attrs={'class':'product_name'})
        # price_data  = data.find_all('div', attrs={'class':'product_price'})
        offer_price = data.find_all('span', attrs={'price'})

        # print(repr(offer_price))

        for products in product_id:
            prod_elems = products.text
            prod_clean = prod_elems.strip('\n')
            product_list.append(prod_clean)
        
        for data in offer_price:
            elems = repr(data.text)
            for elems in data:
                prices.append(elems.translate({ord(i): None for i in '\n\t\t\t'}))
    

        items_map = {
            'Product' : {i: product_list[i] for i in range(1,len(product_list))},
            'Price'   : {i: prices[i] for i in range(len(prices))},
            }

        return items_map
    else:
        print('The HTTP response has the following code -->',page.status_code,sys.exc_info()[0], sys.exc_info()[1])
       

def table(items_map):
    items_map = get_tags(url)
    data = pd.DataFrame().from_dict(data=items_map,orient='columns')

    prod_data  = data.iloc[1:,0]
    price_data = data.iloc[:,1].shift(1)

    result = pd.concat([prod_data,price_data],axis=1)
    beers = result.drop([0],axis=0)
    print(beers)



if __name__ == "__main__":
    url = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16'
    items_map = get_tags(url)
    table(items_map)
    