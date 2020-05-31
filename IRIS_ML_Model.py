from IRISML_DataUtility import DataUtility

from data_load import file
from data_load import csv 
from data_load import path

import pandas as pd
import numpy as np

import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data.dataset import random_split
from torch.autograd import Variable
from torch.utils import data

class LogisticRegression(torch.nn.Module):
    def __init__(self, input_size, output_classes):
        super(LogisticRegression,self).__init__()
        self.linear = torch.nn.Linear(input_size,output_classes)
    
    def forward(self,x):
        y_pred = torch.nn.LogSoftmax(self.linear(x))
        return y_pred

class ParametersUtility:
    def __init__(self,parameters=None):
        self.parameters = dict()

    def get_parameters(self):
        self.parameters = {
            'batch_size'       : 50,
            'shuffle'          : True,
            'lr'               : 0.05,
            'n_iters'          : 5,
        }
        return self.parameters


def _generateTensor(data):
    table = DataUtility.clean_data(data)
    cols  = DataUtility.get_cols(data)
    k = len(cols)
    for columns in cols:
        x_vars = table.loc[:, cols[:k-1]]
        y_vars = table.loc[:, cols[k-1]]
    return Variable(Tensor(x_vars.shape),requires_grad=False), Variable(Tensor(y_vars.shape),requires_grad=False)

def generateTensor_Train(data, request_type):
    """This method converts the data into training and testing split using random split method in torch.
    Upon split, this method then specifies given the request, cast the variable with Tensor and numpy shape attribute. """
    
    table  = DataUtility.clean_data(data)
    train_data, test_data = DataUtility._generate_split(data)
    cols  = DataUtility.get_cols(data)
    k     = len(cols)

    if request_type == "train":
        for i in train_data.indices:
            x_train = table.loc[:i,cols[:k-1]]
            y_train = table.loc[:i,cols[k-1]]
        return Variable(Tensor(x_train.shape),requires_grad=False), Variable(Tensor(y_train.shape),requires_grad=False)

    elif request_type == "test":
        for i in test_data.indices:
            x_test = table.loc[:i,cols[:k-1]]
            y_test = table.loc[:i,cols[k-1]]
        return Variable(Tensor(x_test.shape),requires_grad=False), Variable(Tensor(y_test.shape),requires_grad=False)

    elif request_type is None:
        return "Please specify either Train/Test as valid request types"


def loaderMethod(data,request_type):
    parameters = {
        'batch_size'       : 100,
        'shuffle'          : True,
    }
    if request_type == "train":
        train_data = torch.utils.data.DataLoader(dataset=generateTensor_Train(data,request_type="train"),batch_size=parameters['batch_size'],shuffle=parameters['shuffle'])
        return train_data
    
    if request_type == "test":
        parameters.update(['shuffle',False])
        test_data = torch.utils.data.DataLoader(dataset=generateTensor_Train(data,request_type="test"),batch_size=parameters['batch_size'],shuffle=parameters['shuffle'])
        return test_data

def train(model,optimizer,loss,epochs):
    parameters = {
        'batch_size'       : 50,
        'shuffle'          : True,
        'lr'               : 0.05,
        'n_iters'          : 5,
    }
    train_data = loaderMethod(data,"train")

    x_train, y_train = generateTensor_Train(data,"train")

    for epoch in range(0,epochs+1):
        optimizer.zero_grad()

        #Forward pass:
        y_pred = model.forward(x_train)

        #Calculate loss:
        cost   = loss(y_pred,y_train)
        
        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        cost.backward()
        optimizer.step()
        if (epoch+1) % 100 == 0:
            print ('Epoch: [%d/%d],Loss: %.4f' % (epoch+1,len(train_data)//parameters['batch_size'], loss.data[0]))


if __name__=="__main__":
    data = DataUtility(file(path,csv))
    # for testing only: _generateTensor(data)
    generateTensor_Train(data,request_type = "train")

    parameters   = ParametersUtility().get_parameters() 

    model        = LogisticRegression(input_size=4,output_classes=3)
    optimizer    = torch.optim.SGD(model.parameters(),lr=0.05)
    loss         = torch.nn.CrossEntropyLoss()
    epochs       = parameters['n_iters']*parameters['batch_size']//DataUtility.__len__(data)

    train(model,optimizer,loss,epochs)








