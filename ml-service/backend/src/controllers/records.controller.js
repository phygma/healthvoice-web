const { PrismaClient } = require('@prisma/client');
const fs = require('fs');

const prisma = new PrismaClient();

// ── GET /api/records ────────────────────────────────────────────────────────
// Returns all health records, newest first, capped at 100.
// Frontend records table calls this on page load.
exports.getAllRecords = async (req, res) => {
  try {
    const records = await prisma.healthRecord.findMany({
      orderBy: { createdAt: 'desc' },
      take: 100,
      select: {
        id:             true,
        originalText:   true,
        translatedText: true,
        sourceLang:     true,
        targetLang:     true,
        patientName:    true,
        audioOutputUrl: true,
        createdAt:      true,
      },
    });

    return res.json({
      success: true,
      count: records.length,
      records,
    });

  } catch (err) {
    console.error('getAllRecords error:', err.message);
    return res.status(500).json({ error: 'Failed to fetch records' });
  }
};

// ── GET /api/records/:id ────────────────────────────────────────────────────
// Returns a single health record by its ID.
// Frontend uses this to show full detail of one record.
exports.getRecordById = async (req, res) => {
  try {
    const record = await prisma.healthRecord.findUnique({
      where: { id: req.params.id },
    });

    if (!record) {
      return res.status(404).json({ error: 'Record not found' });
    }

    return res.json({ success: true, record });

  } catch (err) {
    console.error('getRecordById error:', err.message);
    return res.status(500).json({ error: 'Failed to fetch record' });
  }
};

// ── DELETE /api/records/:id ─────────────────────────────────────────────────
// Deletes a health record and its associated audio files.
// Best practice: always clean up files when deleting a DB record,
// otherwise your uploads/ folder fills up with orphaned audio files.
exports.deleteRecord = async (req, res) => {
  try {
    const record = await prisma.healthRecord.findUnique({
      where: { id: req.params.id },
    });

    if (!record) {
      return res.status(404).json({ error: 'Record not found' });
    }

    // Delete associated audio files from disk before removing DB record
    if (record.audioInputUrl && fs.existsSync(record.audioInputUrl)) {
      fs.unlinkSync(record.audioInputUrl);
    }
    if (record.audioOutputUrl && fs.existsSync(record.audioOutputUrl)) {
      fs.unlinkSync(record.audioOutputUrl);
    }

    await prisma.healthRecord.delete({
      where: { id: req.params.id },
    });

    console.log(`🗑️  Deleted record: ${req.params.id}`);
    return res.json({ success: true, deletedId: req.params.id });

  } catch (err) {
    console.error('deleteRecord error:', err.message);
    return res.status(500).json({ error: 'Failed to delete record' });
  }
};