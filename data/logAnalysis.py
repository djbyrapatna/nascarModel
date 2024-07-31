import pandas as pd
from linExport import createTestTrain, importXy, filterXy
from polyAnalysis import createPolyX
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures

def logRegSplits(xFile, yFile):
    X, y = importXy(xFile, yFile)
    X_train, X_test, y_train, y_test = createTestTrain(X,y, scale = None)
    return  X_train, X_test, y_train, y_test

def logRegSetup(y_train, y_test, cutoffArray):
    #X_train, X_test, y_train, y_test = logRegSplits(xFile, yFile)
    yArr = []
    for cutoff in cutoffArray:
        yPair = []
        for y in (y_train,y_test):
            logDf = y.copy()
            logDf.loc[logDf['Pos'] <= cutoff, 'Pos'] = int(1)
            logDf.loc[logDf['Pos'] > cutoff, 'Pos'] = int(0)
            logDf['Pos'].astype('int32', copy=False)
            #y = y.apply(lambda x:1 if x<=cutoff else 0)
            yPair.append(logDf)
        yArr.append(yPair)
    return yArr

def logReg(X_train, X_test, y_train, y_test, model, metrics=False, probs=False):
    #print(y_train.to_numpy().flatten())
    label_encoder = LabelEncoder()
    arr = y_train.to_numpy().flatten()
    arr = label_encoder.fit_transform(arr)
    #print(arr)
    model.fit(X_train, arr)

    # Make predictions
    y_pred = model.predict(X_test)
    metArr = []
    y_prob = None

    testArr = y_test.to_numpy().flatten()
    testArr = label_encoder.fit_transform(testArr)
    # Evaluate the model
    if metrics:
        accuracy = accuracy_score(testArr, y_pred)
        precision = precision_score(testArr, y_pred)
        recall = recall_score(testArr, y_pred)
        f1 = f1_score(testArr, y_pred)
        metArr = [accuracy, precision, recall, f1]
    if probs:
        y_prob = model.predict_proba(X_test)
    return [testArr, y_prob, metArr]

def logRegRun(xFile, yFile, cutOffArray, polyModel = False, degree=2, colList = None, metrics=False, probs=False):
    X_train, X_test, y_train, y_test = logRegSplits(xFile, yFile)
    yArr = logRegSetup(y_train, y_test, cutOffArray)
    #print(len(yArr))
    retArr = []
    model = LogisticRegression()
    if polyModel:
        a,b = filterXy([X_train, X_test], colList)
        X_train, X_test = createPolyX(X_train, X_test, degree=degree)
    for i in range(len(cutOffArray)):
        ret = logReg(X_train, X_test, yArr[i][0], yArr[i][1], model, metrics=metrics, probs=probs)
        retArr.append(ret)
    return retArr




        
