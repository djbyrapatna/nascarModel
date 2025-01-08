from queries import query
from data import linRegModelSetup as ms, taggedDataAnalysis as tda, taggedDataProcess as tdp
import pickle
from os import makedirs
from os.path import dirname
import pandas as pd


currentUnprocessedDataFiles = ["data/racingref/ldatatotal.pkl",
         "data/racingref/pdatatotal.pkl",
         "data/racingref/qdatatotal.pkl"
         ,"data/racingref/rdatatotal.pkl"]

destinationUnprocessDataFiles = currentUnprocessedDataFiles

def updateUnprocessedData(yearMin, yearMax, raceMin, raceMax, inputFiles, outputFiles):
    urls = query.urlGen(yearMin, yearMax, raceMin, raceMax)
    for i, group in enumerate(urls):
        isRace = False
    
        if i == 3:
            isRace=True
        outputDf = query.compileDataset(group,
                    existingDatasetPath=inputFiles[i],removeCertainRaceData=isRace)

        makedirs(dirname(outputFiles[i]), exist_ok=True)
        with open(outputFiles[i], 'wb') as f:
            pickle.dump(outputDf, f)

def updateAndProcessTaggedData(yearMin, yearMax, raceMin, raceMax, excelFileLocation, destinationFileLocation, referenceRaceData):
    tempTrackFiles = ["trackTempTagged.pkl", "teamTempTagged.pkl"]
    tdp.updateTaggedData(excelFileLocation, tempTrackFiles)
    H = tda.createHelperDf(referenceRaceData, raceMin,raceMax,yearMin,yearMax, tempTrackFiles)
    with open("helperTagTemp.pkl", 'wb'):
        pickle.dump(f)
    M = tda.createMainDf("helperTagTemp.pkl")
    with open(destinationFileLocation, 'wb') as f:
        pickle.dump(f)

def combineAllDataForModel(destinationFileLocations, yearMin, yearMax, raceMin, raceMax, 
                        fileArr, includeLoop=False, includeHistoric=False, includeTagged=False,
                        posKeyArr=['Pos', 'Rank', 'Rank'], tagArr=['race', 'prac', 'qual'],
                        currArr=[False, True, True], loopFile = "racingref/forModel/loopDataUntagged.pkl", 
                        historicFileArr = None, taggedFile = None):
    
    X, y = ms.dataForLinRegModel(fileArr, includeLoop, includeHistoric, includeTagged, posKeyArr, tagArr,
    currArr, raceMin, raceMax, yearMin, yearMax, loopFile)
    xLocation, yLocation = destinationFileLocations
    
    with open(xLocation, 'wb') as f:
         pickle.dump(X, f)
   
    with open(yLocation, 'wb') as f:
         pickle.dump(y, f)

def modelUpdate(yearMin, yearMax, raceMin, raceMax, fileArr, **kwargs):
    inputUnprocessedFiles, outputUnprocessedFiles, xModelFile, yModelFile = fileArr
    taggedFile = None
    includeHistoric, includeTagged, includeLoop = False, False, False
    if 'updateTagged' in kwargs and kwargs.get('updateTagged'):
        if 'taggedFileArr' in kwargs:
            excelFileLocation, destinationFileLocation, referenceRaceData = kwargs.get('taggedFileArr')
            taggedFile = destinationFileLocation
            includeTagged=True
        else:
            print('Tagged data file locations not provided')
            return None
        
    if 'historicFileArr' in kwargs:
        historicFileArr = kwargs.get(historicFileArr)
        includeHistoric=True
    else:
        historicFileArr=None

    if 'updateTagged' not in kwargs and 'taggedFile' in kwargs:
        taggedFile = kwargs.get('taggedFile')
        includeTagged=True
    elif 'updateTagged' not in kwargs:
        includeTagged=False
    
    allowedAddnlKeys = ['posKeyArr', 'tagArr', 'currArr', 'loopFile']
    combineKwargs = {key: kwargs[key] for key in allowedAddnlKeys if key in kwargs}
    if 'loopFile' in combineKwargs:
        includeLoop=True

    updateUnprocessedData(yearMin, yearMax, raceMin, raceMax, inputUnprocessedFiles,outputUnprocessedFiles)
    print("Updated Unprocessed Data")
    if 'updateTagged' in kwargs and kwargs.get('updateTagged'):
        updateAndProcessTaggedData(yearMin, yearMax, raceMin, raceMax, excelFileLocation, destinationFileLocation, referenceRaceData)
        print("Updated Tagged Data")
    combineAllDataForModel([xModelFile,yModelFile], yearMin, yearMax, raceMin, raceMax, 
                        fileArr, includeLoop=includeLoop, includeHistoric=includeHistoric, includeTagged=includeTagged, 
                        historicFileArr = historicFileArr, taggedFile = taggedFile, **combineKwargs)
    print("Model data output done")

    


