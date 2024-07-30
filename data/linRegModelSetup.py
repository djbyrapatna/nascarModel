import numpy as np 
import pickle
#import matplotlib.pyplot as plt
from basicAnalysis import dataForRace
import pandas as pd
#import sys
#np.set_printoptions(threshold=sys.maxsize)
# Structure:
# 1. Establish Y data set
#     a. Start with Brickyard 400 results
#     b. Then move back to last 3,4,5, etc (will require change in how I process data)
# 2. Establish X data set
#     a. Prev race results
#     b. Curr race practice and qual results
#     c. All race, practice, qual results
#     d. Loop data only
#     e. Loop and race
#     f. All combined
# After trying with b, figure out how I'd like to proceed

#1a

def dataForLinRegModel(fileArr, posKeyArr, tagArr, raceMin, raceMax, currArr):
    #create y dataframe
    y = pd.DataFrame()
    with open(fileArr[0], 'rb') as f:
        dfY = pickle.load(f)
    f.close()
    for race in range(raceMin, raceMax+1):
        raceKey = race*100+24
        raceOfInterest = dfY[raceKey]
        tmpY = raceOfInterest[['Driver', 'Pos']].copy()
        tmpY['Driver'] = tmpY['Driver']+ '_'+str(race)
        tmpY['Driver'] = tmpY['Driver'].str.strip()
        y = y._append(tmpY)
    #create X dataframe
    X = pd.DataFrame()
    for race in range(raceMin, raceMax+1):
        tmpX = pd.DataFrame()
        for i in range(len(fileArr)):
            fileName = fileArr[i]
            raceKey = race*100+24
            typeX = dataForRace(fileName, posKeyArr[i], race, currArr[i])
            typeX['Driver'] = typeX['Driver']+'_'+str(race)
            typeX.columns = [col +tagArr[i] if col!='Driver' else col for col in typeX.columns]
            typeX['Driver'] = typeX['Driver'].str.strip()
            #print(typeX)
            if tmpX.empty:
                tmpX = tmpX._append(typeX)
                
            else:
                #print(i, "\n", typeX.dtypes, "\n", tmpX.dtypes)
                tmpX = pd.merge(tmpX, typeX, on = 'Driver', how='inner')
            
        #print(tmpX['Driver'].unique())
        X = X._append(tmpX[tmpX['Driver'].isin(y['Driver'])])
    y = y[y['Driver'].isin(X['Driver'])]
    return [X, y]
        

        




# with open("/Users/dhruvajb/Documents/Prog Personal/nascar/nascarModel/data/racingref/rdata.pkl",'rb') as f:
#     dfRace = pickle.load(f)
# f.close()

# raceNums = [15,16,17,18,19,20,21,22]
# y = pd.DataFrame()
# X = pd.DataFrame()
# for race in raceNums:
#     raceKey = race*100+24
#     raceOfInterest = dfRace[raceKey]
#     tmpY = raceOfInterest[['Driver', 'Pos']].copy()
#     tmpX = dataForRace("/Users/dhruvajb/Documents/Prog Personal/nascar/nascarModel/data/racingref/rdata.pkl", 'Pos', race, False)
#     tmpY['Driver'] = tmpY['Driver']+ '_'+str(race)
#     tmpX['Driver'] = tmpX['Driver']+'_'+str(race)
#     y = y._append(tmpY[tmpY['Driver'].isin(tmpX['Driver'])])
#     X = X._append(tmpX[tmpX['Driver'].isin(tmpY['Driver'])])


# from sklearn.model_selection import train_test_split

# unique_values = X['Driver'].unique()
# # Split unique values into training and testing sets
# unique_train, unique_test = train_test_split(unique_values, test_size=0.2)

# #print(unique_train)

# # Use the splits to subset both X and y
# X_train = X[X['Driver'].isin(unique_train)].sort_values('Driver')
# X_test = X[X['Driver'].isin(unique_test)].sort_values('Driver')
# y_train = y[y['Driver'].isin(unique_train)].sort_values('Driver')
# y_test = y[y['Driver'].isin(unique_test)].sort_values('Driver')


# from sklearn.linear_model import LinearRegression
# X_train = X_train.drop('Driver', axis=1)
# X_test = X_test.drop('Driver', axis=1)
# y_train = y_train.drop('Driver', axis=1)
# y_test= y_test.drop('Driver', axis=1)
# model = LinearRegression()




# X_train= X_train.filter(['PrevAll'])
# X_test =X_test.filter(['PrevAll'])
# model.fit(X_train,y_train)

# y_pred = model.predict(X_test)

# from sklearn.metrics import mean_squared_error, r2_score

# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
# print(model.coef_)

# print(f'Mean Squared Error: {mse}')
# print(f'R-squared: {r2}')

