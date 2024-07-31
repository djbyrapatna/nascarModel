import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from polyAnalysis import polyRegRun, polyFeatureRanking
from linAnalysis import linAnalysisRun, linFeatureRanking
from logAnalysis import logRegRun
from statistics import fmean

# model = LinearRegression()
polyColList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
# linAnalysisRun("compiledDataX.pkl", "compiledDataY.pkl",model)

# polyRegRun("compiledDataX.pkl", "compiledDataY.pkl",model,polyColList)

# print(linFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl",model))
# print(polyFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl", model, polyColList, features=7))

model = LogisticRegression()
cutOffArray = [10]

#resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, polyModel=True, colList=polyColList, metrics=True, probs = True)
printArr = ['Accuracy', 'Precision', 'Recall', 'F1']

precArrLin = []
recallArrLin = []
precArrPoly = []
recallArrPoly = []

for i in range(0,10):
    resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, 
                         metrics=True, probs = False)
    precision = resultArr[0][2][1]
    recall = resultArr[0][2][2]
    precArrLin.append(precision)
    recallArrLin.append(recall)



for i in range(0,10):
    resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, 
                          polyModel=True, colList=polyColList, metrics=True, probs = False)
    precision = resultArr[0][2][1]
    recall = resultArr[0][2][2]
    precArrPoly.append(precision)
    recallArrPoly.append(recall)

print("Cutoff position 10")
print("Avg Lin Precision: ", fmean(precArrLin))
print(precArrLin)
print("Avg Lin Recall: ", fmean(recallArrLin))
print(recallArrLin)
print("Avg Poly Precision: ", fmean(precArrPoly))
print(precArrPoly)
print("Avg Poly Recall: ", fmean(recallArrPoly))
print(recallArrPoly)


# for i in range(len(resultArr)):
#     result = resultArr[i]
#     metricsArray = result[2]
#     print("Metrics for Cutoff Position "+str(cutOffArray[i])+ ":")
#     for j in range(len(metricsArray)):
#         print(printArr[j]+ ": "+ str(metricsArray[j]))

