import joblib
import pandas as pd
import os
from workflows.modelManager import ModelManager

def createKey(driver, race, year):
    return f'{driver}_{race}_{year}'

manager = ModelManager(xFile="data/racingref/forModel/compiledDataX.pkl", yFile="data/racingref/forModel/compiledDataY.pkl")

cutoffArray = [1,3,5,10,20]

keyTest = createKey("Chase Elliott", 22,2024)

# p = manager.predictProbability(keyTest,'log',10)

# print(p)

results = manager.predictAllProbabilities(keyTest,['log'],cutoffArray)

for model in results.keys():
    for cutoff in results[model].keys():
        prob = float(results[model][cutoff])
        print(f"Probability of finishing in top {cutoff} is {prob:.2%}")



