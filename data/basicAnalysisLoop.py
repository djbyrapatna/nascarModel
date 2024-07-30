import pandas as pd
import pickle
import numpy as np
from statistics import fmean

#going to import data, then do prev, prev3, ..., season for loop data
#Avg. Pos.	Pass Diff.	Green Flag Passes	Green Flag Times Passed	
# Quality Passes	Pct. Quality Passes	
# Fastest Lap	Top 15 Laps	Pct. Top 15 Laps	
# Laps Led	Pct. Laps Led	Total Laps	DRIVER RATING

def loopDataforRace(fileName, raceNum, includeCurr):
    with open(fileName,'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    colList = list(dfRace[224].columns)[6:]
    driverList = dfRace[124]['Driver']
    retArr = pd.DataFrame()
    for colName in colList:
        posKey = colName
        colName = colName.replace(" ", '').replace(".",'')
        avgStatArray = pd.DataFrame(columns=["Driver", "Prev"+colName, "Prev3"+colName, "Prev5"+colName, "Prev10"+colName, "PrevAll"+colName])
        for driver in driverList:
            statArray = []
            #loop thru races in data set
            for i in range(raceNum,0,-1):
                #get specific dataframe corresponding to race
                key = i*100+24
                d = dfRace[key]
                #find row of data corresponding to driver
                if not d.empty:
                    rowDf = d[d['Driver'] == driver]
                #if row exists, append finish to statArray
                if not rowDf.empty:
                    statArray.append(rowDf[posKey].tolist()[0])
            
            numRaces = len(statArray)
            if numRaces >=10:
                #calculate and append the previous finish, the average finish over the last 3, 5, 10, and total season races
                dfAdd = [driver]
                dfAdd.append(statArray[0])
                if numRaces >=3:
                    prev3 = fmean(statArray[0:3])
                    dfAdd.append(prev3)
                else:
                    dfAdd.append(-1)
                if numRaces >=5:
                    prev5 = fmean(statArray[0:5])
                    dfAdd.append(prev5)
                else:
                    dfAdd.append(-1)
                if numRaces >=10:
                    prev10 = fmean(statArray[0:10])
                    dfAdd.append(prev10)
                else:
                    dfAdd.append(-1)
                dfAdd.append(fmean(statArray))
                #add this to new dataFrame avgStatArray
                avgStatArray.loc[len(avgStatArray)] = dfAdd

        if retArr.empty:
            retArr = retArr._append(avgStatArray)
        else:
            #print(i, "\n", typeX.dtypes, "\n", tmpX.dtypes)
            retArr = pd.merge(retArr, avgStatArray, on = 'Driver', how='inner')
    return retArr




