#%%

# Library Import
import seaborn as sns
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Module Import
import LogisticRegression_ML
from LogisticRegression_ML import main as function

# Graphing Function
def simple_plot(data):
    graph = sns.lineplot(x="epoch",y="accuracy",data=data)
    return graph

def sub_plots(data):
    data = function()
    data.set_index("epoch")
    f, (axis1,axis2) = plt.subplots(1,2)
    data[["loss_train","loss_test"]].plot(ax=axis1)
    data[["accuracy"]].plot(ax=axis2)
    plt.ylim(bottom=0.7)
    return plt.show()

# Run
data = function()
simple_plot(data)
sub_plots(data)


