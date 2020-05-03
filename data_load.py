import pandas as pd 
import json, csv
path = '/Users/taishanlin/Desktop/IRIS ML/'
csv = 'iris.data.csv'

def file(path,csv):
    data = pd.read_csv(path+csv)
    return data 

def csv_json(data):
    data = file(path,csv)
    data_dict = pd.DataFrame(data=data).to_dict(orient='records')
    return data_dict

if __name__ == "__main__":
    data = file(path,csv)
    print(csv_json(data))
