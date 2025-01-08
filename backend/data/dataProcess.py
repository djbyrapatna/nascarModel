import pandas as pd
import numpy as np
import pickle

files = ['racingref/rdata.xlsm', 'racingref/qdata.xlsm', 'racingref/pdata.xlsm', 'racingref/ldata.xlsm']

rDataFile = files[0]

df = pd.read_excel(rDataFile, sheet_name = None, header=None)

df['Sheet1'].columns = ['Pos','St','#','Driver','Sponsor / Owner',	'Car',	'Laps',	'Status','Led','Pts','PPts']

for i in range(len(df.keys())):
    key = list(df.keys())[i]
    df[key].columns = df['Sheet1'].columns
    

for i in range(len(df.keys())):
    key = list(df.keys())[i]
    df[key] = df[key].drop(columns=['Sponsor / Owner', "Pts", "PPts"])
    df[key].dropna(inplace=True)

keyList= list(df.keys())
j = 1
for key in keyList:
    newName = j*100+24
    df[newName] = df.pop(key)
    j+=1

#print(df['Race_3_24'])

with open('racingref/rdata.pkl', 'wb') as f:
    pickle.dump(df, f)

sheetNames = ['Race_', 'Qual_', 'Prac_', 'Loop_']

for k in range(1,4):
    dataFile = files[k]
    df = pd.read_excel(dataFile, sheet_name = None)

 
    keyList= list(df.keys())
    j = 1
    for key in keyList:
        df[key].dropna(inplace=True)
        newName = j*100+24
        df[newName] = df.pop(key)
        j+=1
    testStr = sheetNames[k]+str(4)+"_24"
    
    pklFile = 'racingref/'+dataFile[10:15]+'.pkl'
    with open(pklFile, 'wb') as f:
        pickle.dump(df, f)