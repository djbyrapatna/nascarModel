#need to do following steps
#1. Import historic data and do same processing as other stuff
#a. Combine with current data 
#b. update prevs to incorporate across seasons
#2. Parse historic data seasonwide
#3. Incorporate tagged track data-prev track averages, prev race averages
#4. Incorporate teammate and manufacturer-prevSeason, prev track type avs, etc

import pickle
import pandas as pd
from statistics import fmean

def dataForRace(fileName, posKey, race, yr, includeCurr):
    raceKey = race*100 +(yr%100)
    with open(fileName, 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    #print(dfRace.keys())
    driverList = dfRace[raceKey]['Driver']
    if includeCurr:
        avgFinishes = pd.DataFrame(columns=["Driver", "Year", "Curr", "Prev", 
                                            "Prev3", "Prev5", "Prev10", "PrevAll"])
    else:
        avgFinishes = pd.DataFrame(columns=["Driver", "Year","Prev", 
                                            "Prev3", "Prev5", "Prev10", "PrevAll"])
    
    for driver in driverList:
        finishes = []
        curr = 0
        startRange = race
        if not includeCurr:
            startRange -=1
        #loop thru races in data set
        for i in range(startRange,0,-1):
            #get specific dataframe corresponding to race
            key = i*100 +(yr%100)
            d = dfRace[key]
            

            #find row of data corresponding to driver
            if not d.empty:
                rowDf = d[d['Driver'] == driver]
            #if row exists, append finishes array
            if rowDf.empty and isinstance(driver, str):
                driverSpace = "  "+driver
                rowDf = d[d['Driver'] == driverSpace]
            if not rowDf.empty:
                if i == race:
                    curr = rowDf[posKey].tolist()[0]   
                else:
                    finishes.append(rowDf[posKey].tolist()[0])
    
        numRaces = len(finishes)
        # if isinstance(driver, str):
            #print(driver, len(driver))
        #calculate and append the previous finish, the average finish over the last 3, 5, 10, and total season races
  
        if numRaces>=10:
            dfAdd = [driver,yr]
            if includeCurr:
                #print("here?")
                dfAdd.append(curr)
            #print (finishes)
            #if numRaces>0:
            dfAdd.append(finishes[0])
            #if numRaces >=3:
            prev3 = fmean(finishes[0:3])
            dfAdd.append(prev3)
            # else:
            #     dfAdd.append(-1)
            #if numRaces >=5:
            prev5 = fmean(finishes[0:5])
            dfAdd.append(prev5)
            # else:
            #     dfAdd.append(-1)
            #if numRaces >=10:
            prev10 = fmean(finishes[0:10])
            dfAdd.append(prev10)
            # else:
            #     dfAdd.append(-1)
            dfAdd.append(fmean(finishes))

            avgFinishes.loc[len(avgFinishes)] = dfAdd
            
    
    return avgFinishes

def createSeasonData(fileName, posKey):
    with open(fileName, 'rb') as f:
        dfRace = pickle.load(f)
    f.close()
    yearArray = [2021,2022,2023,2024]
    avgFinishes =  pd.DataFrame(columns=["Driver", "Year",posKey])
    for yr in yearArray:
        raceKey = yr%100 + 100
        driverList = dfRace[raceKey]['Driver']
        
        for driver in driverList:
            avgFinish = []
            endRange = yr%100+3600
            for key in range(raceKey,endRange,100):
                if key in dfRace:
                    d = dfRace[key]
                    if not d.empty:
                        rowDf = d[d['Driver'] == driver]
                    if not rowDf.empty:
                        avgFinish.append(rowDf[posKey].tolist()[0])
            numRaces = len(avgFinish)
            if numRaces>=5:
                dfAdd = [driver,yr]
                #print(dfAdd, avgFinish)
                dfAdd.append(fmean(avgFinish))
                avgFinishes.loc[len(avgFinishes)] = dfAdd
    return avgFinishes

fileArr = ["racingref/rdatatotal.pkl","racingref/pdatatotal.pkl","racingref/qdatatotal.pkl"]
posArr = ["Pos", "Rank", "Rank"]

# for i in range(len(fileArr)):
#     df = createSeasonData(fileArr[i], posArr[i])
#     pklFile = 'racingref/'+fileArr[i][10:15]+'seasonAvg.pkl'
#     with open(pklFile, 'wb') as f:
#         pickle.dump(df, f)

# file = "racingref/ldatatotal.pkl"
# with open(file, 'rb') as f:
#     dfLoop = pickle.load(f)
# posArr = dfLoop[124].columns[6:]
# cols = ["Driver", "Year"] + list(posArr)

# dfOut = pd.DataFrame(columns=cols)
# dfStart = createSeasonData(file,cols[2])
# print (cols)
# dfOut['Driver'] = dfStart['Driver']
# dfOut['Year'] = dfStart['Year']
# dfOut[cols[2]] = dfStart[cols[2]]
# for col in cols[3:]:
#     print(col)
#     dfStart = createSeasonData(file,col)
#     dfOut[col] = dfStart[col]
# dfOut.columns = [col.replace(' ', '').replace('.', '') for col in dfOut.columns]
# print (dfOut.columns)

# pklFile = 'racingref/ldataseasonAvg.pkl'
# with open(pklFile, 'wb') as f:
#     pickle.dump(dfOut, f)

