// nascarModel/backend/nodeApp/src/utils/modelManager.js
const { spawn } = require('child_process');
const path = require('path');

class ModelManager {
  constructor() {
    // Path to the retrieveModelResult.py script in the workflows directory
    this.scriptPath = path.join(__dirname, '../../../workflows/retrieveModelResult.py');
    // Determine the correct Python command
    this.pythonCommand = this.getPythonCommand();
  }

  /**
   * Determines the correct Python command to use.
   * @returns {string} - 'python' or 'python3'
   */
  getPythonCommand() {
    // Attempt to spawn 'python' with version check
    try {
      const version = spawn.sync('python', ['--version']);
      if (version.status === 0 && version.stdout.toString().includes('Python 3')) {
        return 'python';
      }
    } catch (e) {
      // Ignore and try 'python3'
    }

    // Fallback to 'python3'
    return 'python3';
  }

  /**
   * Queries the model by invoking the Python script.
   * @param {string} driverName - Name of the driver.
   * @param {string|number} raceNumber - Race number.
   * @param {string|number} year - Year of the race.
   * @param {string} modelDesc - Model description (e.g., 'log', 'randomforest').
   * @param {number} cutoff - Cutoff value.
   * @returns {Promise<Object>} - Resolves with the prediction result.
   */
  queryModel(driverName, raceNumber, year, modelDesc, cutoff) {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn(this.pythonCommand, [
        this.scriptPath,
        driverName,
        raceNumber,
        year,
        modelDesc,
        cutoff
      ]);

      let data = '';
      let error = '';

      // Capture standard output
      pythonProcess.stdout.on('data', (chunk) => {
        data += chunk.toString();
      });

      // Capture errors
      pythonProcess.stderr.on('data', (chunk) => {
        error += chunk.toString();
      });

      // Handle process closure
      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          // Attempt to parse error message from stdout
          try {
            const errorResponse = JSON.parse(data);
            return reject(`Python script exited with code ${code}: ${errorResponse.error}`);
          } catch (parseError) {
            // Fallback to stderr if JSON parsing fails
            return reject(`Python script exited with code ${code}: ${error}`);
          }
        }
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (parseError) {
          reject(`Error parsing Python output: ${parseError}`);
        }
      });

      // Handle execution errors
      pythonProcess.on('error', (err) => {
        reject(`Failed to start Python script: ${err}`);
      });
    });
  }
}


module.exports = new ModelManager();
