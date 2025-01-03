import pandas as pd
from .linExport import createTestTrain, importXy, filterXy
from .linAnalysis import cleanTotal
from .polyAnalysis import createPolyX
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_class_weight
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
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

"""
    Trains and evaluates models for each cutoff and model type, optionally saving the trained models.

    Parameters:
    - xFile (str): Path to the features data file.
    - yFile (str): Path to the target data file.
    - cutOffArray (list of int): List of cutoff values for label binarization.
    - modelType (str, default='log'): Type of model to train ('log', 'randomforest', 'xgBoost', 'svm').
    - scale (str or None, default=None): Scaling method ('zScale' for StandardScaler, etc.).
    
    - **kwargs: Additional keyword arguments:
        - clean (bool, default=False): Whether to clean the data.
        - dropPractice (bool, default=False): Whether to drop practice-related columns.
        - metrics (bool, default=False): Whether to compute evaluation metrics.
        - probs (bool, default=False): Whether to return probability predictions.
        - saveModels (bool, default=False): Whether to save the trained models.
        - modelDir (str, default='models'): Directory to save the models.
        - degree (int, default=2): Degree for polynomial features if polyModel is True.
        - colList (list of str or None, default=None): List of columns to use for polynomial features.

    Returns:
    - list: A list of results for each cutoff, where each result contains [testArr, y_prob, metArr].
"""
def logRegRun(xFile, yFile, cutOffArray, modelType='log', scale = None,
             **kwargs):
    
    #Setup and process data
    kwargKeys = ['clean', 'dropPractice', 'metrics', 'probs', 'saveModels', 'polyModel']
    clean, dropPractice, metrics, probs, saveModels, polyModel = [kwargs.get(key, False) for key in kwargKeys]
    degree = kwargs.get('degree', 2)
    modelDir = kwargs.get('modelDir', 'models')
    colList = kwargs.get('colList', None)

    X_train, X_test, y_train, y_test = logRegSplits(xFile, yFile,scale=None, clean=clean, dropPractice=dropPractice)
    yArr = logRegSetup(y_train, y_test, cutOffArray)

    retArr = []
    
    if saveModels:
        #ensure directory exists, create folder if necessary
        if not path.exists(modelDir):
            makedirs(modelDir)

    #choose model and set up addnl parameters as necessary
    svmFlag = False
    baseModel = LogisticRegression()
    if modelType=='randomforest':
        baseModel = RandomForestClassifier()
    elif modelType =='xgBoost':
        baseModel = xgb.XGBClassifier()
    elif modelType=='svm':
        svmFlag = True

   
    if polyModel and colList is not None:
    # Create a transformer that applies PolynomialFeatures to specified columns
        polyTransformer = ColumnTransformer(
            transformers=[
                ('poly', PolynomialFeatures(degree=degree, include_bias=False), colList)
            ],
            remainder='passthrough'  # Keep the rest of the columns unchanged
        )
    else:
        polyTransformer = 'passthrough'  # No polynomial features

    #run model for each cutoff in cutoffArray, append results
    for i, cutoff in enumerate(cutOffArray):
        if svmFlag:
            class_weights = compute_class_weight('balanced', 
                classes=np.unique(yArr[i][0].values.flatten()), y=yArr[i][0].values.flatten())
            class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
            classifier = SVC(kernel='rbf',class_weight=class_weight_dict,probability=True)
        else:
            classifier=baseModel

        # Define preprocessing steps
        preprocessingSteps = [
            ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values
            ('poly', polyTransformer),  # Apply polynomial features if required
        ]
        # Add scaling to the Pipeline if required
        if scale == 'zScale':
            preprocessingSteps.append(('scaler', StandardScaler()))
        elif scale == 'minMaxScale':
            preprocessingSteps.append(('scaler', MinMaxScaler()))
        else:
            preprocessingSteps.append(('scaler', 'passthrough'))  # No scaling

        # Create the Pipeline with preprocessing and classifier
        pipeline = Pipeline(preprocessingSteps + [('classifier', classifier)])
        # Train the pipeline
        result = logReg(X_train, X_test, yArr[i][0], yArr[i][1], pipeline, metrics=metrics, probs=probs)
        retArr.append(result)

        if saveModels:
            if not dropPractice:
                modelFilename = f"{modelType}_cutoff_{cutoff}.pkl"
            else:
                modelFilename = f"{modelType}_no_prac_cutoff_{cutoff}.pkl"
            modelPath = path.join(modelDir, modelFilename)
            joblib.dump(pipeline, modelPath)
            print(f"Saved model: {modelPath}")

    return retArr




        
