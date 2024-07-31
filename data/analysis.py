import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from polyAnalysis import polyRegRun, polyFeatureRanking
from linAnalysis import linAnalysisRun, linFeatureRanking
from logAnalysis import logRegRun

# model = LinearRegression()
# polyColList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
# linAnalysisRun("compiledDataX.pkl", "compiledDataY.pkl",model)

# polyRegRun("compiledDataX.pkl", "compiledDataY.pkl",model,polyColList)

# print(linFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl",model))
# print(polyFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl", model, polyColList, features=7))

model = LogisticRegression()
cutOffArray = [1,3,5,10,20]

resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, metrics=True, probs = True)
printArr = ['Accuracy', 'Precision', 'Recall', 'F1']

for i in range(len(resultArr)):
    result = resultArr[i]
    metricsArray = result[2]
    print("Metrics for Cutoff Position "+str(cutOffArray[i])+ ":")
    for j in range(len(metricsArray)):
        print(printArr[j]+ ": "+ str(metricsArray[j]))

