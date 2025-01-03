import joblib
import pandas as pd
import os
import pickle


class ModelManager:
    def __init__(self, xFile, yFile, modelDir='../data/savedModels'):
        """
        Initializes the ModelManager by loading the dataset and preparing it for queries.

        Parameters:
        - xFile (str): Path to the features data file.
        - yFile (str): Path to the target data file.
        - modelDir (str, default='saved_models'): Directory where models are saved.
        """
        self.modelDir = modelDir
        self.xFile = xFile
        self.yFile = yFile
        self.loadData()
        self.prepareData()
    
    def loadData(self):
        """
        Loads the dataset into memory.
        """
        with open(self.xFile,'rb') as f:
            self.X_full = pickle.load(f)
       
        # Assuming 'Driver' column contains keys in the format 'DriverName_RaceNumber_Year'
        self.X_full.set_index('Driver', inplace=True)
    
    def prepareData(self):
        """
        Prepares the data for querying by ensuring the index is set correctly.
        """
        # Ensure that the 'Driver' column is set as the index for faster lookup
        if 'Driver' not in self.X_full.index.names:
            self.X_full.set_index('Driver', inplace=True)
    
    def loadModel(self, modelDesc, cutoff, noPrac):
        """
        Loads a trained model from disk.

        Parameters:
        - modelDesc (str): Unioque model identifier (e.g.) ('log', 'log_no_prac','randomforest', 'xgBoost', 'svm').
        - cutoff (int): The cutoff value.

        Returns:
        - Pipeline: The loaded Scikit-learn Pipeline model.
        """
        if noPrac:
            modelFilename = f"{modelDesc}_no_prac_cutoff_{cutoff}.pkl"
        else:
            modelFilename = f"{modelDesc}_cutoff_{cutoff}.pkl"
        modelPath = os.path.join(self.modelDir, modelFilename)
        
        if not os.path.exists(modelPath):
            raise FileNotFoundError(f"Model file '{modelFilename}' not found in directory '{self.modelDir}'.")
        
        pipeline = joblib.load(modelPath)
        return pipeline
    
    def predictProbability(self, key, modelDesc, cutoff):
        """
        Predicts the probability that the result associated with the given key is within the cutoff limit.

        Parameters:
        - key (str): The unique identifier in the format 'DriverName_RaceNumber_Year' (e.g., 'Chase Elliott_11_2022').
        - modelType (str): Type of the model ('log', 'randomforest', 'xgBoost', 'svm').
        - cutoff (int): The cutoff value.

        Returns:
        - float: Probability that the result is within the cutoff limit.
        """
        if key not in self.X_full.index:
            raise ValueError(f"No data found for key: '{key}'. Please check the key and try again.")
        
        row = self.X_full.loc[[key]]  
        hasBlankColumns = row.isnull().any(axis=1).iloc[0]
        
        try:
            pipeline = self.loadModel(modelDesc, cutoff, noPrac=hasBlankColumns)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Failed to load model for key '{key}': {e}")
        
        # Predict the probability
        try:
            prob = pipeline.predict_proba(row)[0][1]  # Probability of class 1
        except Exception as e:
            raise RuntimeError(f"Error during prediction for key '{key}': {e}")
        
        return prob
    
    def predictAllProbabilities(self, key, modelTypes, cutoffs):
        """
        Predicts probabilities across multiple models and cutoff values for a given key.

        Parameters:
        - key (str): The unique identifier in the format 'DriverName_RaceNumber_Year'.
        - modelTypes (list of str): List of model types ('log', 'randomforest', 'xgBoost', 'svm').
        - cutoffs (list of int): List of cutoff values.

        Returns:
        - dict: Nested dictionary with model types and cutoffs mapping to predicted probabilities.
        """
        results = {}
        for modelDesc in modelTypes:
            results[modelDesc] = {}
            for cutoff in cutoffs:
                try:
                    prob = self.predictProbability(key, modelDesc, cutoff)
                    results[modelDesc][cutoff] = prob
                except Exception as e:
                    results[modelDesc][cutoff] = str(e)
        return results
