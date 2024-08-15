import pandas as pd
import numpy as np
import pickle

tagArray = ["race", "practice", "qual", "loop"]
fileArray = ["racingref/rdatahistoric.xlsm","racingref/pdatahistoric.xlsm","racingref/qdatahistoric.xlsm","racingref/ldatahistoric.xlsm"]

for file in fileArray:
    df = pd.read_excel(file, sheet_name = None)
    for i in range(len(df.keys())):
        key = list(df.keys())[i]
        if df[key].columns[0] != df['Sheet1'].columns[0]:
            print("Column error at sheet ", key, " in file ", file)
        colsToDrop = ['Sponsor / Owner', "Pts", "PPts"]
        df[key] = df[key].drop(columns=[col for col in colsToDrop if col in df[key].columns])
    keyList= list(df.keys())
    j = 1
    for key in keyList:
        newName = ((j-1)%36+1)*100+(21+(j-1)//36)
        df[newName] = df.pop(key)
        j+=1
    pklFile = 'racingref/'+file[10:15]+'total.pkl'
    with open(pklFile, 'wb') as f:
        pickle.dump(df, f)
        