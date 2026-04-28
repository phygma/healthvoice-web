const router = require('express').Router();
const axios = require('axios');

// GET /api/health
// Returns the status of this backend AND the ML service.
// Useful for: frontend dashboard ("Is the system ready?"),
// debugging connection issues, smoke tests.
router.get('/', async (req, res) => {
  let mlStatus = 'down';
  try {
    await axios.get(`${process.env.ML_SERVICE_URL}/health`, { timeout: 2000 });
    mlStatus = 'up';
  } catch {
    // ML service not running — that's expected during early dev.
    // Don't crash, just report 'down'.
  }

  res.json({
    status: 'ok',
    backend: 'up',
    mlService: mlStatus,
    mockMode: process.env.USE_MOCK_ML === 'true',
    timestamp: new Date().toISOString(),
  });
});

module.exports = router;