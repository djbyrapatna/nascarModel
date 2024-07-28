import pandas as pd
import pickle
import numpy as np
from statistics import fmean

pklFiles = ['racingref/pdata','racingref/rdata'  ,'racingref/qdata']

for fileName in pklFiles:
    with open(fileName+".pkl", 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    posKey = 'Rank'
    if fileName == pklFiles[1]:
        posKey = 'Pos'
    #print(dfRace)
    driverList = dfRace[424]['Driver']

    avgFinishes = pd.DataFrame(columns=["Driver", "Prev", "Prev3", "Prev5", "Prev10", "PrevAll"])

    for driver in driverList:
        finishes = []
        for i in range(21,0,-1):
            key = i*100+24
            d = dfRace[key]
            print(d)
            if not d.empty:
                rowDf = d[d['Driver'] == driver]
            if not rowDf.empty:
                finishes.append(rowDf[posKey].tolist()[0])
        numRaces = len(finishes)
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
        #print (finishes)
        avgFinishes.loc[len(avgFinishes)] = dfAdd
    outputFileName = fileName+"comp"
    with open(outputFileName, 'wb') as f:
        pickle.dump(avgFinishes, f)
    f.close()
    print(avgFinishes)


    





