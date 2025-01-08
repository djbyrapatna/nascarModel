from .query import urlGen, compileDataset
import pickle
from os import makedirs, path

urls = urlGen(2024,2024,22,36)

filesFinal = ["../data/racingref/forModel/loopDataUntagged.pkl",
         "../data/racingref/forModel/pracDataUntagged.pkl",
         "../data/racingref/forModel/qualDataUntagged.pkl"
         ,"../data/racingref/forModel/raceDataUntagged.pkl"]

filesToLoad = ["../data/racingref/ldatatotal.pkl",
         "../data/racingref/pdatatotal.pkl",
         "../data/racingref/qdatatotal.pkl"
         ,"../data/racingref/rdatatotal.pkl"]


for i, group in enumerate(urls):
    isRace = False
  
    if i == 3:
        isRace=True
    outputDf = compileDataset(group,existingDatasetPath=filesToLoad[i],removeCertainRaceData=isRace)

    makedirs(path.dirname(filesFinal[i]), exist_ok=True)
    with open(filesFinal[i], 'wb') as f:
        pickle.dump(outputDf, f)



