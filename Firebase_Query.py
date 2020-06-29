import firebase_admin
from   collections import OrderedDict
from   firebase_admin import credentials
from   firebase_admin import db
from   firebase_admin import firestore

import sys
import numpy as np
import pandas as pd

cred = credentials.Certificate("/Users/taishanlin/Documents/Heavy Drinking Dataset/bar-crawl-classification-firebase-adminsdk-71pyp-a8f4a3f127.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bar-crawl-classification.firebaseio.com/'
})

def ordered_getkeys():
    data = {}
    alcohol = db.reference('Data').order_by_key().get()
    for k in alcohol:
       data = {k:alcohol[k] for k in range(len(alcohol))}
    #print(data)
    return data

def search(key,search_term):
    library = ordered_getkeys()
    print("The search term is {0}, the value is -> ".format(search_term),library[key]["'{0}'".format(search_term)])
    
def search_attributes(search_term):
    mykey = 0
    myvalue = 0
    try:
        for key,value in data.items():
            mykey = key
            myvalue = data[mykey]["'{}'".format(search_term)]
            print("Search {}|".format(search_term), "The key is {0} & the value returned is {1}".format(key,myvalue))
    except:
        print("error type ->",sys.exc_info()[0],"please check if search term provided exists")
    return myvalue

if __name__ == "__main__":
    data = ordered_getkeys()
    #search(110,'Color intensity')
    search_attributes('Hue')

        
    
        
    
            

    