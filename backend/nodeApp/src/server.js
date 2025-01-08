const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const modelRoutes = require('./routes/modelRoutes');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors({
    origin: 'http://localhost:3000' // Specify your frontend's origin
  }));
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
