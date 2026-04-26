const router = require('express').Router();
const {
  getAllRecords,
  getRecordById,
  deleteRecord,
} = require('../controllers/records.controller');

// GET /api/records — all health records, newest first
router.get('/', getAllRecords);

// GET /api/records/:id — single record by ID
router.get('/:id', getRecordById);

// DELETE /api/records/:id — delete a record
router.delete('/:id', deleteRecord);

module.exports = router;