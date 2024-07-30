import numpy as np 
import pickle
import pandas as pd
from linRegModelSetup import dataForLinRegModel
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

def createTestTrain(X, y):
    unique_values = X['Driver'].unique()
    # Split unique values into training and testing sets
    unique_train, unique_test = train_test_split(unique_values, test_size=0.2)
    # Use the splits to subset both X and y
    X_train = (X[X['Driver'].isin(unique_train)].sort_values('Driver')).drop('Driver', axis=1)
    X_test = (X[X['Driver'].isin(unique_test)].sort_values('Driver')).drop('Driver', axis=1)
    y_train = (y[y['Driver'].isin(unique_train)].sort_values('Driver')).drop('Driver', axis=1)
    y_test = (y[y['Driver'].isin(unique_test)].sort_values('Driver')).drop('Driver', axis=1)
    return X_train, X_test, y_train, y_test


fileArr = ["/Users/dhruvajb/Documents/Prog Personal/nascar/nascarModel/data/racingref/rdata.pkl", 
           "/Users/dhruvajb/Documents/Prog Personal/nascar/nascarModel/data/racingref/pdata.pkl",
           "/Users/dhruvajb/Documents/Prog Personal/nascar/nascarModel/data/racingref/qdata.pkl"]

raceMin = 15
raceMax = 22
posKeyArr = ['Pos', 'Rank', 'Rank']
currArr = [False, True, True]
tagArr = ['race','prac','qual']

X, y = dataForLinRegModel(fileArr, posKeyArr, tagArr, raceMin,raceMax,currArr)

X_train, X_test, y_train, y_test = createTestTrain(X,y)

#print(X_train, y_train)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
#X_train= X_train.filter(['Currqual'])
#X_test =X_test.filter(['Currqual'])
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(model.coef_)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')