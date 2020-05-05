# Pytorch Library
# Variable is the input & output class
# Transform is a class specifically to handle data manipulation
# Data set is a utility class 
import torch 
from torch.utils import data
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


#https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel 
################################################################
#Custom Data Loader Class
#Pre-processing
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
            y_train     = df_train.drop(['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'], axis=1)
            x_train     = df_train.drop([' IRIS Class '], axis=1)
            return x_train, y_train
        elif request_type == "test_data":
            test_data   = self._load_data('test_data')
            df_test     = pd.DataFrame(test_data)
            y_test      = df_train.drop(['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width'], axis=1)
            x_test      = df_test.drop([' IRIS Class '], axis=1)
            return x_test, y_test
    
################################################################################################################################
class Dataset(data.Dataset):
    def __init__(self, list_IDs, labels):
        self.list_IDs = list_IDs 
        self.labels   = labels

    def __getitem__(self,index):
        ID = self.list_IDs[index]
        
        x_variable = torch.load(ID)
        y_variable = self.labels[ID]

        return x_variable, y_variable
        
    def __len__(self):
        #'Denotes the total number of samples'
        return len(self.list_IDs)


class LogisticRegression(torch.nn.Module):
    def _init__(self,input_dimension, output_dimension):
        super(LogisticRegression,self).__init__()
        self.linear = torch.nn.Linear(input_dimension,output_dimension)

    def forward(self,x):
        outputs = torch.nn.Softmax(self.linear(x))
        return outputs 


class ModelParameters:
    def __init__(self,batch_size = None, n_iters = None, lrn_rate = None,input_dimension=None, output_dimension = None,parameters=None,numworkers=None):
        self.batch_size       = batch_size #10 
        self.n_iters          = n_iters #1000 
        self.lrn_rate         = lrn_rate #0.05
        self.input_dimension  = input_dimension #596 # 4 variables * 149 
        self.output_dimension = output_dimension #447 # 3 variables * 149
        self.shuffle          = False 
        self.parameters       = dict()
        self.numworkers       = numworkers

    def get_params(self):
        self.parameters = {
            'batch_size' : self.batch_size,
            'n_iters'    : self.n_iters,
            'lrn_rate'   : self.lrn_rate,
            'shuffle'    : True,
            'num_workers': self.numworkers,
        }
        return self.parameters
    
    def get_epoch(self,dataset):
        data  = Data_Loader(dataset=dataset)
        epoch = self.n_iters * self.batch_size/len(data)
        return epoch





class Optimize(torch.optim.SGD):
    def __init__(self, model,batch_size, n_iters, lrn_rate,input_dimension, output_dimesnsion,parameters,numworkers):
        super().__init__(lrn_rate)
        self.model = LogisticRegression()
    




    
    
