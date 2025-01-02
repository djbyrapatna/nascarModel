import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from polyAnalysis import polyRegRun, polyFeatureRanking
from linAnalysis import linAnalysisRun, linFeatureRanking
from logAnalysis import logRegRun
from statistics import fmean
from linExport import importXy
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
import numpy as np

float_formatter = "{:.4f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})
# X, y = importXy("racingref/formodel/compiledDataX.pkl", "racingref/formodel/compiledDatay.pkl" )

# not_in_Y = X[~X['Driver'].isin(y['Driver'])]['Driver']
# duplicates = X[X['Driver'].duplicated(keep=False)]
# X.iloc[:, 1:-5] = X.iloc[:, 1:-5].apply(lambda x: pd.to_numeric(x, errors='coerce')).astype('float64')
# column_types = X.dtypes
# print(column_types)
# numBlanks = X.isnull().any(axis=1).sum()
# print(numBlanks)
#model = LinearRegression()
polyColList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
#coeff_df= linAnalysisRun("racingref/compiledDataXtotal.pkl", "racingref/compiledDataytotal.pkl",model, clean=True, printOption=True)


#coeff_df=polyRegRun("racingref/compiledDataXtotal.pkl", "racingref/compiledDataytotal.pkl",model,polyColList,  clean=True,printOption=True)
# print("\n\n\nLin Features -------------------------------")
# print(linFeatureRanking("racingref/compiledDataXtotal.pkl", "racingref/compiledDataytotal.pkl",model, features = 15, clean=True))
#print(polyFeatureRanking("racingref/compiledDataXtotal.pkl", "racingref/compiledDataytotal.pkl", model, polyColList, features=7, clean=True))

model = LogisticRegression()
cutOffArray = [1,3,5,10,20]

# resultArr = logRegRun("racingref/forModel/compiledDataX.pkl", "racingref/forModel/compiledDataY.pkl",
#                       cutOffArray, modelType='log', scale = None,metrics=True, probs = True, clean=True)
printArr = ['Accuracy', 'Precision', 'Recall', 'F1']



modelTypeAndScale = [['log', None]]

n = len(cutOffArray)

res = [[]*n for _ in range(len(modelTypeAndScale))]

for j in range(len(modelTypeAndScale)):
    ms = modelTypeAndScale[j]
    m, s = ms
    print(m)
    print(printArr)
    precArray = [[] for _ in range(n)]
    for a in range(20):
        if (a+1)%5==0:
            print("Iteration ", a+1)
        resultArr = logRegRun("racingref/formodel/compiledDataX.pkl", "racingref/formodel/compiledDataY.pkl",
                        cutOffArray, modelType=m, scale = s,metrics=True, probs = True, clean=True, dropPractice=True)
        numCutoffs = len(resultArr)
        for i in range(len(resultArr)):
            result = resultArr[i]
            yprob = result[1]
            metricsArray = result[2]
            precArray[i].append(metricsArray[1])
            print(metricsArray, f" Cutoff: {cutOffArray[i]}")
    for i in range(len(precArray)):
        mean = fmean(precArray[i])
        res[j].append(mean)

print(res)

# precArrLin = []
# recallArrLin = []
# precArrPoly = []
# recallArrPoly = []

# for i in range(0,10):
#     resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, 
#                          metrics=True, probs = False)
#     precision = resultArr[0][2][1]
#     recall = resultArr[0][2][2]
#     precArrLin.append(precision)
#     recallArrLin.append(recall)



# for i in range(0,10):
#     resultArr = logRegRun("compiledDataX.pkl", "compiledDataY.pkl",cutOffArray, 
#                           polyModel=True, colList=polyColList, metrics=True, probs = False)
#     precision = resultArr[0][2][1]
#     recall = resultArr[0][2][2]
#     precArrPoly.append(precision)
#     recallArrPoly.append(recall)

# print("Cutoff position 10")
# print("Avg Lin Precision: ", fmean(precArrLin))
# print(precArrLin)
# print("Avg Lin Recall: ", fmean(recallArrLin))
# print(recallArrLin)
# print("Avg Poly Precision: ", fmean(precArrPoly))
# print(precArrPoly)
# print("Avg Poly Recall: ", fmean(recallArrPoly))
# print(recallArrPoly)


# for i in range(len(resultArr)):
#     result = resultArr[i]
#     metricsArray = result[2]
#     print("Metrics for Cutoff Position "+str(cutOffArray[i])+ ":")
#     for j in range(len(metricsArray)):
#         print(printArr[j]+ ": "+ str(metricsArray[j]))

