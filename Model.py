# Pytorch Library
# Variable is the input & output class
# Transform is a class specifically to handle data manipulation
# Data set is a utility class 
import torch
from torch import Tensor
import pandas as pd
import torchvision.transforms as transforms
import torchvision.datasets as datasets

from torch.utils.data.dataset import random_split
from torch.autograd import Variable
from torch.utils import data

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
        #map_ = y_table.to_dict('index')
        return y_table

    #contruct the clean dataset
    def __len__(self):
        return len(self.clean_data())

    def clean_data(self):
        return self.dataset
    
    def _generate_split(self):
        lengths                = [int(len(self.dataset)*0.8), int(len(self.dataset)*0.2)]
        train,test             = torch.utils.data.random_split(self.dataset,lengths)
        print(train.indices,test.indices)
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

        
class LogisticRegression(torch.nn.Module):
    def _init__(self,input_dim,output_dim):
        super(LogisticRegression,self).__init__()
        self.linear = torch.nn.Linear(input_dim,output_dim)

    def forward(self,x):
        outputs = torch.nn.Softmax(self.linear(x))
        return outputs 


class Dataset(data.Dataset):
    def __init__(self, list_IDs, labels):
        self.list_IDs = list_IDs 
        self.labels   = labels #flower labels

    def __getitem__(self,index):
        ID = self.list_IDs[index]
        
        x_variable = torch.load('data/' + ID + '.pt')
        y_variable = self.labels[ID]

        return x_variable, y_variable
        
    def __len__(self):
        #'Denotes the total number of samples'
        return len(self.list_IDs)


def train(model,optimizer,loss,x_variable,y_variable, epoch):
    for i in range(epoch):
        for local_batch, local_labels in training_generator:
            model.train()
            optimizer.zero_grad()
            
            #Forward pass:
            y_pred = model.forward(x_variable)

            #Calculate loss:
            cost   = loss(y_pred,y_variable)
            if i % 100 == 99:
                print(i, cost.item())
            
            # Zero gradients, perform a backward pass, and update the weights.
            optimizer.zero_grad()
            cost.backward()
            optimizer.step()
    print("End Operation")

class ModelParameters:
    def __init__(self,batch_size,shuffle,numworkers, n_iters,lr,input_dimension,output_dimension):
        self.batch_size       = batch_size #10 
        self.n_iters          = n_iters #1000 
        self.lr               = lr #0.05
        self.input_dimension  = input_dimension #596 # 4 variables * 149 
        self.output_dimension = output_dimension #447 # 3 variables * 149
        self.shuffle          = False
        self.numworkers       = numworkers

    def get_params(self):
        self.parameters = {
            'batch_size' : self.batch_size,
            'shuffle'    : True,
            'num_workers': self.numworkers,
        }
        return self.parameters
    
    def get_epoch(self,dataset):
        data  = DataUtility(dataset=dataset)
        epoch = self.n_iters * self.batch_size/len(data)
        return epoch

if __name__ == "__main__":
    dataset = DataUtility(dataset=file(path,csv))

    xs                 = dataset.generate_partition("train_data")
    ys                 = list(dataset.generate_labels("train_data"))


    x_variable         = Variable(Tensor(xs),requires_grad=False)
    y_variable         = Variable(Tensor(ys),requires_grad=False)


    parameters = ModelParameters(
        batch_size       = 50,
        lr               = 0.05,
        n_iters          = 1000,
        input_dimension  = 594,
        output_dimension = 447,
        numworkers       = 6,
        shuffle          = True,
    )

    script_params = parameters.get_params()
    epoch = parameters.get_epoch(dataset)
    #max_epoch = 100

    training_set       = Dataset(x_variable,y_variable)
    training_generator = torch.utils.data.DataLoader(training_set,**script_params)

    model        = LogisticRegression()
    optimizer    = torch.optim.SGD(model.parameters(),lr=0.05)
    loss         = torch.nn.CrossEntropyLoss()
    ## Looping over epochs
    train(model,optimizer,loss,x_variable,y_variable,epoch)


            


