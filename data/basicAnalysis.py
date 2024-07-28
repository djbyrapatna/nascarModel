import pandas as pd
import pickle
import numpy as np
from statistics import fmean

pklFiles = ['racingref/pdata','racingref/rdata'  ,'racingref/qdata']

for fileName in pklFiles:
    #open pickle file
    with open(fileName+".pkl", 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    posKey = 'Rank'
    if fileName == pklFiles[1]:
        posKey = 'Pos'
    #get driver list
    driverList = dfRace[424]['Driver']

    avgFinishes = pd.DataFrame(columns=["Driver", "Prev", "Prev3", "Prev5", "Prev10", "PrevAll"])

    for driver in driverList:
        finishes = []
        #loop thru races in data set
        for i in range(21,0,-1):
            #get specific dataframe corresponding to race
            key = i*100+24
            d = dfRace[key]
            #print(d)
            #find row of data corresponding to driver
            if not d.empty:
                rowDf = d[d['Driver'] == driver]
            #if row exists, append finish to finishes
            if not rowDf.empty:
                finishes.append(rowDf[posKey].tolist()[0])
        numRaces = len(finishes)
        #calculate and append the previous finish, the average finish over the last 3, 5, 10, and total season races
        dfAdd = [driver]
        dfAdd.append(finishes[0])
        if numRaces >=3:
            prev3 = fmean(finishes[0:3])
            dfAdd.append(prev3)
        else:
            dfAdd.append(-1)
        if numRaces >=5:
            prev5 = fmean(finishes[0:5])
            dfAdd.append(prev5)
        else:
            dfAdd.append(-1)
        if numRaces >=10:
            prev10 = fmean(finishes[0:10])
            dfAdd.append(prev10)
        else:
            dfAdd.append(-1)
        dfAdd.append(fmean(finishes))
        #add this to new dataFrame avgFinishes
        avgFinishes.loc[len(avgFinishes)] = dfAdd
    #write new dataframe avgFinishes to new file
    outputFileName = fileName+"comp.pkl"
    with open(outputFileName, 'wb') as f:
        pickle.dump(avgFinishes, f)
    f.close()
    print(avgFinishes)


    





