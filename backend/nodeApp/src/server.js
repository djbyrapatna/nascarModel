const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const modelRoutes = require('./routes/modelRoutes');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/model', modelRoutes);

// Root Endpoint
app.get('/', (req, res) => {
  res.send('Backend is running');
});

// Start Server
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
