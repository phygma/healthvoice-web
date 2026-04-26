const router = require('express').Router();
const { handleDiagnose } = require('../controllers/diagnose.controller');

// POST /api/diagnose
// Body: JSON { symptomText, sourceLang, recordId? }
router.post('/', handleDiagnose);

module.exports = router;