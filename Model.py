# Pytorch Library
# Variable is the input & output class
# Transform is a class specifically to handle data manipulation
# Data set is a utility class 
import torch 
import pandas as pd
from torch.autograd import Variable
import torchvision.transforms as transforms
import torchvision.datasets as datasets

from data_load import file
from data_load import csv 
from data_load import path

# Step 1. Load Dataset
# Step 2. Make Dataset Iterable
# Step 3. Create Model Class
# Step 4. Instantiate Model Class
# Step 5. Instantiate Loss Class
# Step 6. Instantiate Optimizer Class
# Step 7. Train Model

class Data_Loader:
    def __init__(self, dataset):
        self.dataset = dataset

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
            elif i == 'Iris-virginica':
                y_variable.append(2)
            else:
                y_variable.append(3)
        y_table = pd.DataFrame(y_variable,columns=['IRIS ID']).join(target)
        #map_ = y_table.to_dict('index')
        return y_table

    def clean_data(self):
        input   = self._get_inputs()
        output  = self._get_target()
        dataset = input.join(output)
        return dataset


    def _load_data(self,request_type):
        self.dataset           = self.clean_data()
        train_portion          = 0.6*len(self.dataset)
        test_portion           = len(self.dataset) - train_portion
        train_data             = torch.utils.data.random_split(self.dataset,[int(train_portion)])
        test_data              = torch.utils.data.random_split(self.dataset,[int(test_portion)])
        if request_type   == "train_data":
            return train_data
        elif request_type == "test_data":
            return test_data

    def load_features(self,request_type):
        if request_type == "train_data":
            train_data  = self._load_data('train_data')
            df_train    = pd.DataFrame(train_data)
            x_train     = df_train.drop([' IRIS Class '], axis=1)
            return x_train
        elif request_type == "test_data":
            test_data   = self._load_data('test_data')
            df_test     = pd.DataFrame(test_data)
            x_test      = df_test.drop([' IRIS Class '], axis=1)
            return x_test
    

class LogisticRegression(torch.nn.Module):
    def _init__(self,input_dimension, output_dimension):
        super(LogisticRegression,self).__init__()
        self.linear = torch.nn.Linear(input_dimension,output_dimension)

    def forward(self,x):
        outputs = torch.nn.Softmax(self.linear(x))
        return outputs 


class ModelParameters:
    def __init__(self,batch_size = None, n_iters = None, lrn_rate = None,input_dimension=None, output_dimension = None):
        self.batch_size       = None #10 
        self.n_iters          = None #1000 
        self.lrn_rate         = None #0.05
        self.input_dimension  = None #596 # 4 variables * 149 
        self.output_dimension = None #447 # 3 variables * 149 

    def get_epoch(self,dataset):
        data  = Data_Loader(dataset=dataset)
        epoch = self.n_iters * self.batch_size/len(data)
        return epoch


def main():
    batch_size       = ModelParameters(batch_size = 10)
    n_iters          = ModelParameters(n_iters = 1000)
    lrn_rate         = ModelParameters(lrn_rate = 0.05)
    input_dimension  = ModelParameters(input_dimension = 596)
    output_dimension = ModelParameters(output_dimension = 447)

    model            = LogisticRegression()
    loss             = torch.nn.CrossEntropyLoss()
    optimize         = torch.optim.SGD(params=model.parameters(),lr=lrn_rate)
    x_variables      = Data_Loader(dataset=file(path,csv)).load_features(request_type='train_data')




        
if __name__=="__main__":
    raw        = file(path,csv)
    data       = Data_Loader(dataset=raw)
    #print(data.load_data())


    
    
