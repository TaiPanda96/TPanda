import firebase_admin
from   firebase_admin import credentials
from   firebase_admin import db
from   firebase_admin import firestore

## Load the data
from data_load import csv_json
from data_load import path
from data_load import csv 
from data_load import file


## Configurations
cred = credentials.Certificate("/Users/taishanlin/Desktop/Virtual_Env/IRIS ML/iris-machine-learning-firebase-admin-privatekey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iris-machine-learning.firebaseio.com/'
})

#firebase-adminsdk-p95fe@iris-machine-learning.iam.gserviceaccount.com
def push():
    iris = db.reference('/')
    iris.set({'Flower': 
        {'Data':csv_json(file(path,csv))}
    })

if __name__ == "__main__":
    push()