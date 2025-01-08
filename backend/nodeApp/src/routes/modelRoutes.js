// nascarModel/backend/nodeApp/src/routes/modelRoutes.js
const express = require('express');
const router = express.Router();
const { getModelResponse } = require('../controllers/modelController');

// POST /api/model/query
router.post('/query', getModelResponse);

module.exports = router;
