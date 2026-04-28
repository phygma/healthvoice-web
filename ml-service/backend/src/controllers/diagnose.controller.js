const diagnosisService = require('../services/diagnosis.service');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

exports.handleDiagnose = async (req, res) => {
  const { symptomText, sourceLang, recordId } = req.body;

  // ── Validation ────────────────────────────────────────────────────────
  if (!symptomText || symptomText.trim() === '') {
    return res.status(400).json({ error: 'symptomText is required' });
  }

  const validLangs = ['hi', 'bn', 'ta', 'te', 'mr'];
  if (!sourceLang || !validLangs.includes(sourceLang)) {
    return res.status(400).json({
      error: `sourceLang required. Must be one of: ${validLangs.join(', ')}`
    });
  }

  console.log(`\n🩺 Diagnosis request`);
  console.log(`   Text: "${symptomText.substring(0, 60)}..."`);
  console.log(`   Lang: ${sourceLang}`);

  try {
    // ── Call diagnosis service ────────────────────────────────────────
    const { diagnosis, latencyMs } = await diagnosisService.getDiagnosis(
      symptomText,
      sourceLang
    );

    // ── Save to HealthRecord if recordId provided ─────────────────────
    if (recordId) {
      try {
        await prisma.healthRecord.update({
          where: { id: recordId },
          data: { diagnosis },
        });
        console.log(`   💾 Diagnosis saved to record: ${recordId}`);
      } catch (dbErr) {
        // Non-fatal — still return diagnosis even if DB update fails
        console.warn('   ⚠️  Could not save to record:', dbErr.message);
      }
    }

    return res.json({
      success: true,
      diagnosis,
      latencyMs,
      savedToRecord: !!recordId,
    });

  } catch (err) {
    console.error('❌ Diagnosis error:', err.message);
    return res.status(500).json({
      error: 'Diagnosis failed',
      detail: err.message,
    });
  }
};