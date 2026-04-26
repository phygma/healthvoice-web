require('dotenv').config();
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const path = require('path');
const fs = require('fs-extra');

const healthRoute = require('./routes/health.route');
const translateRoute = require('./routes/translate.route');
const app = express();

// Ensure uploads directory exists
fs.ensureDirSync(process.env.UPLOAD_DIR || './uploads');

// Middleware
app.use(cors({ origin: process.env.FRONTEND_URL }));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static audio files (TTS output served directly to browser)
app.use('/audio', express.static(path.join(__dirname, '../uploads')));

// Routes
app.use('/api/health', healthRoute);
app.use('/api/translate', translateRoute);

// 404 handler — anything that didn't match a route
app.use((req, res) => {
  res.status(404).json({ error: 'Not found', path: req.path });
});

// Global error handler — catches any unhandled errors in routes
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: err.message || 'Internal server error' });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
  console.log(`   Health check: http://localhost:${PORT}/api/health`);
  console.log(`   Mock ML mode: ${process.env.USE_MOCK_ML === 'true' ? 'ON' : 'OFF'}`);
});