import pickle
from .linRegModelSetup import dataForLinRegModel
from sklearn.model_selection import train_test_split
import pandas as pd

def createTestTrain(X, y, **kwargs):
    unique_values = X['Driver'].unique()
    # Split unique values into training and testing sets
    unique_train, unique_test = train_test_split(unique_values, test_size=0.2)
    # Use the splits to subset both X and y
    scale = kwargs.get('scale', None)
    X_train = (X[X['Driver'].isin(unique_train)].sort_values('Driver')).drop('Driver', axis=1)
    X_test = (X[X['Driver'].isin(unique_test)].sort_values('Driver')).drop('Driver', axis=1)
    y_train = (y[y['Driver'].isin(unique_train)].sort_values('Driver')).drop('Driver', axis=1)
    y_test = (y[y['Driver'].isin(unique_test)].sort_values('Driver')).drop('Driver', axis=1)
    dataArr = [X_train, X_test, y_train, y_test]
    cols = X_train.columns
    retArr = []
    if scale:
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.preprocessing import StandardScaler
        scaler = None
        if (scale != "minMaxScale" and scale != "zScale"):
            print("Scaling method not recognized. No scaling applied")
            return dataArr
        elif scale == "minMaxScale":
            scaler = MinMaxScaler()
        else:
            scaler = StandardScaler()
        for i in range(0,2):
            #print(dataArr[i])
            df = scaler.fit_transform(dataArr[i])
            df = pd.DataFrame(df, columns = cols)
            retArr.append(df)
        retArr.append(y_train)
        retArr.append(y_test)
        return retArr
    else:
        return dataArr

def importXy(xFileName, yFileName):
    with open(xFileName,'rb') as f:
        X = pickle.load(f)
    f.close()
    with open(yFileName,'rb') as f:
        y = pickle.load(f)
    f.close()
    return X,y

def dataForLinRegModelExport(fileArr, includeLoop, exportX, exportY, posKeyArr=['Pos', 'Rank', 'Rank'], tagArr=['race', 'prac', 'qual'],
                        currArr=[False, True, True], raceMin=11, raceMax=22, **kwargs):
    fileName="racingref/ldata.pkl"
    includeCurr = False
    colsToKeep = ["Prev10"]
    if kwargs.get('loopFile'):
        fileName = kwargs['loopFile']
    if kwargs.get('includeCurr'):
        includeCurr = kwargs['includeCurr']
    if kwargs.get('colsToKeep'):
        colsToKeep = kwargs['colsToKeep']
    X, y = dataForLinRegModel(fileArr, True, posKeyArr=posKeyArr, tagArr=tagArr,
                        currArr=currArr, raceMin=raceMin, raceMax=raceMax,loopFile=fileName, 
                        includeCurr=includeCurr, colsToKeep = colsToKeep)

    with open(exportX, 'wb') as f:
        pickle.dump(X, f)
    f.close()

    with open(exportY, 'wb') as f:
        pickle.dump(y, f)
    f.close()

def filterXy(dataArr, colList):
    regex_pattern = '|'.join([f"^{col}$" for col in colList])
    retArr = []
    for i in range(len(dataArr)):
        df =dataArr[i].filter(regex=regex_pattern)
        retArr.append(df)
    return retArr

# dataForLinRegModelExport()
