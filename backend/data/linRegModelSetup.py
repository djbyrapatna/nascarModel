import numpy as np 
import pickle
#import matplotlib.pyplot as plt
from .historicAnalysis import dataForRace
from .basicAnalysisLoop import loopDataforRace
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
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

#updated design
#flags for loop, historic, and tagged data
#Need to change races to take in year and race

#calculate bounds for raceKey
def createRaceKeyArray(raceMin, raceMax, yrMin, yrMax):
    raceKeyArray = []
    for yr in range(yrMin, yrMax+1):
        minKey = raceMin*100+yr%100
        if yr == yrMax:
            maxKey = (raceMax)*100+yr%100
        else:
            maxKey = 3600+yr%100
        keyRangeInYr = range(minKey, maxKey+100, 100)
        raceKeyArray.extend(keyRangeInYr)
    return raceKeyArray


def createY(df, raceKeyArray):
    y = pd.DataFrame()
    #create Y dataframe holding drivers tagged by race and yr
    for raceKey in raceKeyArray:
        raceNum = raceKey//100
        yr = raceKey%100 + 2000
        raceOfInterest = df[raceKey]
        tmpY = raceOfInterest[['Driver', 'Pos']].copy()
        tmpY['Driver'] = tmpY['Driver']+'_'+str(raceNum)+'_'+str(yr)
        tmpY['Driver'] = tmpY['Driver'].str.strip()
        y = y._append(tmpY)
    return y    

def dataForLinRegModel(fileArr, includeLoop=True, includeHistoric=True, includeTagged=True,
                       posKeyArr=['Pos', 'Rank', 'Rank'], tagArr=['race', 'prac', 'qual'],
                        currArr=[False, True, True], raceMin=11, raceMax=22, yrMin=2024, yrMax = 2024, **kwargs):
    #create blank dataframe
    with open(fileArr[0], 'rb') as f:
        dfY = pickle.load(f)
    f.close()

    raceKeyArray = createRaceKeyArray(raceMin, raceMax, yrMin, yrMax)
    y = createY(dfY, raceKeyArray)
    
    if includeHistoric:
        if 'historicFileArr' in kwargs:
            historicFileArr = kwargs.get('historicFileArr')
        dfH = []
        for hFile in historicFileArr:
            with open(hFile, "rb") as f:
                hdf = pickle.load(f)
            dfH.append(hdf)
    if includeTagged:
        if 'taggedFile' in kwargs:
            taggedFile = kwargs.get('taggedFile')
        
        with open(taggedFile, "rb") as f:
            dft = pickle.load(f)

    #create X dataframe
    X = pd.DataFrame()

    #now need to iterate thru races and add data
    
    for raceKey in raceKeyArray:
        raceNum = raceKey//100
        yr = raceKey%100 + 2000
        tmpX = pd.DataFrame()
        for i in range(len(fileArr)):
            fileName = fileArr[i]
            typeX = dataForRace(fileName, posKeyArr[i], raceNum, yr, currArr[i])
            
            #This code block incorporates the historic data season averages into the dataframe
            if includeHistoric and yr!=2021:
                hdf = dfH[i]
                #Find season avg data for previous year and add to dataframe. str strip needed to remove
                #white spaces in driver name and match columns
                filteredHDF = hdf[hdf['Year']==yr-1]
                typeX['Driver'] = typeX['Driver'].str.strip()
                filteredHDF['Driver'] = filteredHDF['Driver'].str.strip()
                merged_df = pd.merge(typeX, filteredHDF[['Driver', 'AvgFinish']], on='Driver', how='left')
                # Rename the AvgFinish column to PrevSeasonFinish
                merged_df.rename(columns={'AvgFinish': 'PrevSeason'}, inplace=True)
                typeX['PrevSeason'] = merged_df['PrevSeason'] #add column to typeX
                #Calculate cumulative season avg and add to dataframe in same manner as above
                avg_finish = hdf[hdf['Year'] < yr].groupby('Driver')['AvgFinish'].mean().reset_index()
                avg_finish.rename(columns={'AvgFinish': 'PrevTotal'}, inplace=True)
                avg_finish['Driver'] = avg_finish['Driver'].str.strip()
                # Merge the average AvgFinish to typeX
                typeX = pd.merge(typeX, avg_finish, on='Driver', how='left')


            typeX['Driver'] = typeX['Driver']+'_'+str(raceNum)+'_'+str(yr)
            typeX.columns = [col +tagArr[i] if col!='Driver' else col for col in typeX.columns]
            typeX['Driver'] = typeX['Driver'].str.strip()
            if tmpX.empty:
                tmpX = tmpX._append(typeX)
            else:
                if typeX.empty:
                # Add necessary columns to tmpX if typeX is empty
                    typeX = pd.DataFrame({'Driver': tmpX['Driver']})
                    for col in typeX.columns.difference(['Driver']):
                        typeX[col] = pd.NA
                tmpX = pd.merge(tmpX, typeX, on = 'Driver', how='inner')

        if includeLoop:
            fileName = kwargs.get('loopFile')
            if fileName == None:
                print("Need loop file name")
                break
            includeCurr = kwargs.get('includeCurr', False)
            colsToKeep = kwargs.get('colsToKeep', ["Prev10"])
            regex_pattern = '|'.join([f"({col})" for col in colsToKeep])
            typeX = typeX.filter(regex=regex_pattern)
            typeX = loopDataforRace(fileName, raceNum, yr, includeCurr)
            if includeHistoric and yr !=2021:
                hdf = dfH[3]
                metrics = hdf.columns.difference(['Driver', 'Year'])
                # Columns to calculate averages for

                # Calculate prev year averages
                prev_year_averages = hdf[hdf['Year'] == yr-1].groupby('Driver')[metrics].mean().reset_index()
                prev_year_averages.columns = ['Driver'] + ['PrevSeason'+col for col in prev_year_averages.columns if col != 'Driver']

                # Calculate prev total averages
                prev_total_averages = hdf[hdf['Year'] < yr].groupby('Driver')[metrics].mean().reset_index()
                prev_total_averages.columns = ['Driver'] + ['PrevTotal'+col for col in prev_total_averages.columns if col != 'Driver']

                # Merge the prev year averages with typeX
                typeX = pd.merge(typeX, prev_year_averages, on='Driver', how='left')

                # Merge the prev total averages with typeX
                typeX = pd.merge(typeX, prev_total_averages, on='Driver', how='left')


            typeX['Driver'] = typeX['Driver']+'_'+str(raceNum)+'_'+str(yr)
            typeX.columns = [col +'loop' if col!='Driver' else col for col in typeX.columns]
            typeX['Driver'] = typeX['Driver'].str.strip()
            colsToKeep.append('Driver')
            
            
            if tmpX.empty:
                if raceNum>10:
                    print("Should not reach here")
                tmpX = tmpX._append(typeX)
            else:
                #print(i, "\n", typeX.dtypes, "\n", tmpX.dtypes)
                tmpX = pd.merge(tmpX, typeX, on = 'Driver', how='inner')
        if includeTagged and not tmpX.empty:
            tmpX[['DriverName', 'Race', 'Year']] = tmpX['Driver'].str.split('_', expand=True)
            dft['Driver']= dft['Driver'].str.strip()
            
            # tmpX.to_excel(f'tmpxcheck{raceNum}.xlsx')
            # dft.to_excel(f'dftcheck{raceNum}.xlsx')
            tmpX['Year'] = pd.to_numeric(tmpX['Year'])
            tmpX['Race'] = pd.to_numeric(tmpX['Race'])
            dft['Year'] = pd.to_numeric(dft['Year'])
            dft['Race'] = pd.to_numeric(dft['Race'])
            tmpX.rename(columns = {"Driver":"Driverstring", "DriverName":"Driver"}, inplace=True)
            tmpX = tmpX.merge(dft, on=['Driver',"Year", "Race"], how='left')
            tmpX = tmpX.drop(columns=['Driver', 'Race', 'Year'])
            tmpX.rename(columns={"Driverstring": "Driver"}, inplace=True)
            
        X = X._append(tmpX[tmpX['Driver'].isin(y['Driver'])])

        print("Race ", raceNum, "in year ", yr, " imported")
    y = y[y['Driver'].isin(X['Driver'])]

    return [X, y]
        
fileArr = ["racingref/forModel/raceDataUntagged.pkl","racingref/forModel/pracDataUntagged.pkl","racingref/forModel/qualDataUntagged.pkl"]

# with open(fileArr[0], 'rb') as f:
#     df = pickle.load(f)

# # print(df[2224])
# # print(df[2324])

historicFileArr = ["racingref/rdataSeasonAvg.pkl", "racingref/qdataSeasonAvg.pkl",
                           "racingref/pdataSeasonAvg.pkl","racingref/ldataSeasonAvg.pkl",]

taggedFile = "racingref/mainTagData2.pkl"
# X, y= dataForLinRegModel(fileArr, includeLoop=True, includeHistoric=True, includeTagged=True,
#                        posKeyArr=['Pos', 'Rank', 'Rank'], tagArr=['race', 'prac', 'qual'],
#                         currArr=[False, True, True], raceMin=1, raceMax=36, yrMin=2021, 
#                         yrMax = 2024, loopFile = "racingref/forModel/loopDataUntagged.pkl")



# X.to_excel("Xcheck.xlsx")
# y.to_excel("ycheck.xlsx")

# pklFile = 'racingref/formodel/compiledDataX.pkl'
# with open(pklFile, 'wb') as f:
#     pickle.dump(X, f)
# pklFile = 'racingref/formodel/compiledDataY.pkl'
# with open(pklFile, 'wb') as f:
#     pickle.dump(y, f)
