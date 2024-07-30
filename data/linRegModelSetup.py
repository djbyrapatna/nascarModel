import numpy as np 
import pickle
#import matplotlib.pyplot as plt
from basicAnalysis import dataForRace
from basicAnalysisLoop import loopDataforRace
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

def dataForLinRegModel(fileArr, includeLoop, posKeyArr=['Pos', 'Rank', 'Rank'], tagArr=['race', 'prac', 'qual'],
                        currArr=[False, True, True], raceMin=11, raceMax=22, **kwargs):
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
            if tmpX.empty:
                tmpX = tmpX._append(typeX)
            else:
                #print(i, "\n", typeX.dtypes, "\n", tmpX.dtypes)
                tmpX = pd.merge(tmpX, typeX, on = 'Driver', how='inner')
            
        if includeLoop:
            fileName = kwargs.get('loopFile')
            if fileName == None:
                print("Need loop file name")
                break
            includeCurr = kwargs.get('includeCurr', False)
            colsToKeep = kwargs.get('colsToKeep', ["Prev10"])
            typeX = loopDataforRace(fileName, race, includeCurr)
            #print(typeX)
            typeX['Driver'] = typeX['Driver']+'_'+str(race)
            typeX.columns = [col +'loop' if col!='Driver' else col for col in typeX.columns]
            typeX['Driver'] = typeX['Driver'].str.strip()
            colsToKeep.append('Driver')
            regex_pattern = '|'.join([f"({col})" for col in colsToKeep])
            typeX = typeX.filter(regex=regex_pattern)
            if tmpX.empty:
                print("Should not reach here")
                tmpX = tmpX._append(typeX)
            else:
                #print(i, "\n", typeX.dtypes, "\n", tmpX.dtypes)
                tmpX = pd.merge(tmpX, typeX, on = 'Driver', how='inner')
        X = X._append(tmpX[tmpX['Driver'].isin(y['Driver'])])
        print("Race ", race, "imported")
    y = y[y['Driver'].isin(X['Driver'])]

    return [X, y]
        
