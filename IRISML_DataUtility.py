import torch
import pandas as pd

from data_load import file
from data_load import csv 
from data_load import path

class DataUtility:
    def __init__(self, dataset):
        self.dataset   = dataset
        self.partition = dict()
        self.labels    = dict()

    def _get_inputs(self):
        data = self.dataset
        x_vars = data.drop([' IRIS Class '], axis=1)
        return x_vars

    def _get_target(self):
        data = self.dataset
        target = data[' IRIS Class ']
        y_variable = []
        for i in target:
            if i == 'Iris-setosa':
                y_variable.append(1)
            elif i == 'Iris-versicolor':
                y_variable.append(2)
            elif i == 'Iris-virginica':
                y_variable.append(3)
        y_table = pd.DataFrame(y_variable,columns=['IRIS ID']).join(target)
        return y_table

    #contruct the clean dataset
    def __len__(self):
        return len(self.clean_data())

    def get_cols(self):
        cols = []
        data = self.dataset
        for columns in data.columns:
            cols.append(columns)
        return cols

    def clean_data(self):
        return self.dataset
    
    def _generate_split(self):
        lengths                = [int(len(self.dataset)*0.8), int(len(self.dataset)*0.2)]
        train,test             = torch.utils.data.random_split(self.dataset,lengths)
        #print(train.indices,test.indices)
        return train,test

    def generate_partition(self,request):
        train, test = self._generate_split()

        if request   == "train_data":
            self.partition['train'] = [i for i in range(len(train))]
            return self.partition['train']
        elif request == "test_data":
            self.partition['test'] = [i for i in range(len(test))]
            return self.partition['test']

    def generate_labels(self,request):
        train, test = self._generate_split()
        data = self._get_target()
        target = data['IRIS ID']

        if request   == "train_data":
            self.labels = {i:target[i] for i in range(len(train))} 
            return self.labels.items()
        elif request == "test_data":
            self.labels = {i:target[i] for i in range(len(test))} 
            return self.labels.items()

if __name__=="__main__":
    data = DataUtility(file(path,csv))
    data.clean_data()