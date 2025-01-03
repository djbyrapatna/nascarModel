import os
import sys



project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from data.logAnalysis import logRegRun


cutOffArray = [1,3,5,10,20]

logRegRun(xFile="../data/racingref/formodel/compiledDataX.pkl", yFile="../data/racingref/formodel/compiledDataY.pkl",
                    cutOffArray=cutOffArray, modelType='log', scale = None,
                    metrics=True, probs = True, clean=True, dropPractice=False, saveModels=True)


logRegRun(xFile="../data/racingref/formodel/compiledDataX.pkl", yFile="../data/racingref/formodel/compiledDataY.pkl",
                    cutOffArray=cutOffArray, modelType='log', scale = None,
                    metrics=True, probs = True, clean=True, dropPractice=True, saveModels=True)


logRegRun(xFile="../data/racingref/formodel/compiledDataX.pkl", yFile="../data/racingref/formodel/compiledDataY.pkl",
                    cutOffArray=cutOffArray, modelType='randomforest', scale = None,
                    metrics=True, probs = True, clean=True, dropPractice=False, saveModels=True)

logRegRun(xFile="../data/racingref/formodel/compiledDataX.pkl", yFile="../data/racingref/formodel/compiledDataY.pkl",
                    cutOffArray=cutOffArray, modelType='randomforest', scale = None,
                    metrics=True, probs = True, clean=True, dropPractice=True, saveModels=True)

