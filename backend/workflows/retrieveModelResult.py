# nascarModel/backend/workflows/retrieveModelResult.py

import sys
import json
import os

# Adjust the path to import modelManager from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelManager import ModelManager

def createKey(driver, race, year):
    return f'{driver}_{race}_{year}'

def main():
    if len(sys.argv) != 6:
        print(json.dumps({"error": "Incorrect number of arguments. Expected: driverName raceNumber year modelDesc cutoff"}))
        sys.exit(1)

    driver_name = sys.argv[1]
    race_number = sys.argv[2]
    year = sys.argv[3]
    model_desc = sys.argv[4]
    cutoff = sys.argv[5]

    try:
        # Create the key
        key = createKey(driver_name, race_number, year)

        # Define paths to data files and model directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        x_file = os.path.join(script_dir, '../data/racingref/forModel', 'compiledDataX.pkl')
        y_file = os.path.join(script_dir, '../data/racingref/forModel', 'compiledDataY.pkl')
        model_dir = os.path.join(script_dir, 'models')

        # Initialize ModelManager
        manager = ModelManager(xFile=x_file, yFile=y_file, modelDir=model_dir)

        # Convert cutoff to integer
        cutoff = int(cutoff)

        # Predict probability
        prob = manager.predictProbability(key=key, modelDesc=model_desc, cutoff=cutoff)
        
        # Output result as JSON
        print(json.dumps({"probability": prob}))

    except Exception as e:
        
        error_message = str(e)
        print(json.dumps({"error": error_message}))
        sys.exit(1)

if __name__ == "__main__":
    main()
