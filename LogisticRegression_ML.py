import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch import tensor
print("torch", torch.__version__)
from torchvision import datasets, transforms
from tqdm import tqdm
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelBinarizer


class Net(torch.nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.layer1 = nn.Linear(4,3)

    def forward(self,x):
        output = self.layer1(x)
        return F.log_softmax(output,dim=-1)
    

def instantiate():
    model_parameters = {
        'BATCH_SIZE' : 64,
        'TEST_BATCH_SIZE' : 64,
        'N_EPOCHS' : 2000,
    }

    m            = torch.nn.LogSoftmax(dim=1)
    model        = Net()
    optimizer    = torch.optim.SGD(model.parameters(),lr=0.05)
    loss         = torch.nn.NLLLoss()

    return [model, optimizer, loss, model_parameters,m]


def train(Xtrain, Ytrain, Xtest, Ytest,model,optimizer,loss):
    x_train  = Variable(torch.from_numpy(Xtrain))
    y_train  = Variable(torch.from_numpy(Ytrain.astype(np.int64)))

    x_test   = Variable(torch.from_numpy(Xtest))
    y_test   = Variable(torch.from_numpy(Ytest.astype(np.int64)))
    performance = []

    training_        = instantiate()
    k                = len(training_)
    model_parameters = training_[k-2]

    #print(x_train,y_train)

    for epoch in range(1,model_parameters['N_EPOCHS']+1):
        optimizer.zero_grad()

        #Forward pass:
        y_pred = model.forward(x_train)

        #Calculate loss:
        cost   = loss(y_pred,y_train)
        
        cost.backward()


        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.step()

        #Scoring
        y_test_perf = model(x_test)
        loss_test   = loss(y_test_perf,y_test)
        
        pred_ = y_test_perf.data.max(1,keepdim=True)[1] # this actually extracts the tensor indices of a maximized value.
        # if you use 0 instead of 1, you just extract the max value. Here, you extract the indices of the max value.

        accuracy = pred_.eq(y_test.data.view_as(pred_)).cpu().sum().item()/Ytest.size
        
        performance.append([epoch, cost.data.item(), loss_test.data.item(),accuracy])

    # set index method allows you to specify which column should be the index.
    #result = pd.DataFrame(data=performance,columns=['epoch', 'loss_train', 'loss_test','accuracy']).set_index('epoch')
    result = pd.DataFrame(data=performance,columns=['epoch', 'loss_train', 'loss_test','accuracy'])
    #print(result)
    return result


def main():
    X, Y = load_iris(return_X_y=True)
    X = X.astype("float32")
    ftrain = np.arange(X.shape[0]) % 4 !=0
    #print(ftrain)

    Xtrain, Ytrain = X[ftrain, :],  Y[ftrain]
    Xtest, Ytest   = X[~ftrain, :], Y[~ftrain]
    print(Xtrain.shape, Ytrain.shape, Xtest.shape, Ytest.shape)
    Xtrain.shape, Ytrain.shape, Xtest.shape, Ytest.shape


    training_parameters = instantiate()
    i = 0
    model     = training_parameters[0] 
    loss      = training_parameters[1]
    optimizer = training_parameters[2]
    return train(Xtrain, Ytrain, Xtest, Ytest,model,loss,optimizer)

