import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from polyAnalysis import polyRegRun, polyFeatureRanking
from linAnalysis import linAnalysisRun, linFeatureRanking

model = LinearRegression()
polyColList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
linAnalysisRun("compiledDataX.pkl", "compiledDataY.pkl",model)

polyRegRun("compiledDataX.pkl", "compiledDataY.pkl",model,polyColList)

print(linFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl",model))
print(polyFeatureRanking("compiledDataX.pkl", "compiledDataY.pkl", model, polyColList, features=7))



