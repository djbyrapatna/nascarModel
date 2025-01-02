import pandas as pd
from linExport import createTestTrain, importXy, filterXy
from linAnalysis import cleanTotal
from polyAnalysis import createPolyX
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import xgboost as xgb
import joblib
from os import makedirs, path


#Import xdata (driver key and associated data for each race) and 
#y data (driver key and finishes), clean it (drop unnec.empty cols)
#and create test and train sets
def logRegSplits(xFile, yFile,scale=None, clean=False,dropPractice=False):
    X, y = importXy(xFile, yFile)

    if clean:
        X, y = cleanTotal(X,y, dropPractice=dropPractice)

    X_train, X_test, y_train, y_test = createTestTrain(X,y, scale = scale)
    return  X_train, X_test, y_train, y_test

#Convert y data into 0 to 1 binary representing if driver position
#was within cutoff position
def logRegSetup(y_train, y_test, cutoffArray):
    yArr = []
    #loop through each cutoff
    for cutoff in cutoffArray:
        yPair = []
        for y in (y_train,y_test):
            logDf = y.copy()
            logDf.loc[logDf['Pos'] <= cutoff, 'Pos'] = int(1)
            logDf.loc[logDf['Pos'] > cutoff, 'Pos'] = int(0)
            logDf['Pos'].astype('int32', copy=False)

            yPair.append(logDf)
        yArr.append(yPair)
    return yArr

#Fit and make predictions on model, then evaluate model metrics if indicated by caller
def logReg(X_train, X_test, y_train, y_test, model, metrics=False, probs=False):

    label_encoder = LabelEncoder()
    arr = y_train.to_numpy().flatten()
    arr = label_encoder.fit_transform(arr)
    #train model
    model.fit(X_train, arr)

    # Make predictions
    y_pred = model.predict(X_test)
    metArr = []
    y_prob = None

    #Convert testArr into model output format for comparisons, return
    testArr = y_test.to_numpy().flatten()
    testArr = label_encoder.fit_transform(testArr)
   
    if metrics:
        # Evaluate the model
        accuracy = accuracy_score(testArr, y_pred)
        precision = precision_score(testArr, y_pred)
        recall = recall_score(testArr, y_pred)
        f1 = f1_score(testArr, y_pred)
        metArr = [accuracy, precision, recall, f1]
    if probs:
        #return expected probs of result falling w/in cutoff
        y_prob = model.predict_proba(X_test)
    return [testArr, y_prob, metArr]

#Model pipeline
#1. Create training and test data, and convert y data into position binary for evaluation
#2. Select and set up appropriate model
#3. Run model and return/save results for each cutoff in the cutoffArray
def logRegRun(xFile, yFile, cutOffArray, modelType='log', scale = None,
               colList = None, **kwargs):
    #Setup and process data
    kwargKeys = ['clean', 'dropPractice', 'metrics', 'probs', 'saveModels', 'polyModel']
    clean, dropPractice, metrics, probs, saveModels, polyModel = [kwargs.get(key, False) for key in kwargKeys]

    X_train, X_test, y_train, y_test = logRegSplits(xFile, yFile,scale=scale, clean=clean, dropPractice=dropPractice)
    yArr = logRegSetup(y_train, y_test, cutOffArray)

    retArr = []
    
    if saveModels:
        #ensure directory exists, create folder if necessary
        modelDir = kwargs.get('modelDir', 'models')
        if not path.exists(modelDir):
            makedirs(modelDir)

    #choose model and set up addnl parameters as necessary
    svmFlag = False
    model = LogisticRegression()
    if modelType=='randomforest':
        model = RandomForestClassifier()
    elif modelType =='xgBoost':
        model = xgb.XGBClassifier()
    elif modelType=='svm':
        svmFlag = True

    if polyModel:
        degree = 2
        if 'degree' in kwargs:
            degree = kwargs.get('degree')
        a,b = filterXy([X_train, X_test], colList)
        X_train, X_test = createPolyX(X_train, X_test, degree=degree)

    #run model for each cutoff in cutoffArray, append results
    for i, cutoff in enumerate(cutOffArray):
        if svmFlag:
            class_weights = compute_class_weight('balanced', 
                classes=np.unique(yArr[i][0].values.flatten()), y=yArr[i][0].values.flatten())
            class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
            model = SVC(kernel='rbf',class_weight=class_weight_dict,probability=True)

        ret = logReg(X_train, X_test, yArr[i][0], yArr[i][1], model, metrics=metrics, probs=probs)
        retArr.append(ret)

        if saveModels:
            modelFilename = f"{modelType}_cutoff_{cutoff}.pkl"
            modelPath = path.join(modelDir, modelFilename)
            joblib.dump(model, modelPath)
            print(f"Saved model: {modelPath}")

    return retArr




        
