// nascarModel/backend/nodeApp/src/controllers/modelController.js
const modelManager = require('../utils/modelManager');

/**
 * Handles POST requests to query the model.
 * Expects JSON body with driverName, raceNumber, year, modelDesc, and cutoff.
 */
const getModelResponse = async (req, res) => {
  try {
    const { driverName, raceNumber, year, modelDesc, cutoff } = req.body;

    // Validate required parameters
    if (!driverName || !raceNumber || !year || !modelDesc || cutoff === undefined) {
      return res.status(400).json({
        error: 'Missing required parameters: driverName, raceNumber, year, modelDesc, cutoff'
      });
    }

    // Query the model
    const response = await modelManager.queryModel(driverName, raceNumber, year, modelDesc, cutoff);

    // Check for errors in the Python script response
    if (response.error) {
      return res.status(500).json({ error: response.error });
    }

    // Send the successful response
    res.json(response);
  } catch (error) {
    console.error('Error in getModelResponse:', error);
    res.status(500).json({ error: 'Model query failed', details: error.toString() });
  }
};

module.exports = { getModelResponse };
