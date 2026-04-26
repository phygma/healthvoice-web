// Translation pipeline: Audio → ASR → NMT → TTS → Save to DB → Respond
//
// This controller is the heart of the project. It coordinates three ML
// steps in sequence, saves the result as a HealthRecord, and returns
// everything the frontend needs in one response.
require('dotenv').config();
const mlService = require('../services/ml.service');
const { PrismaClient } = require('@prisma/client');
const path = require('path');
const fs = require('fs');

const prisma = new PrismaClient();

exports.handleTranslate = async (req, res) => {
  const { sourceLang, targetLang, patientName } = req.body;
  const audioFile = req.file;

  // ── Input validation ────────────────────────────────────────────────────
  if (!audioFile) {
    return res.status(400).json({ error: 'No audio file uploaded' });
  }
  if (!sourceLang) {
    return res.status(400).json({ error: 'sourceLang is required' });
  }
  if (!targetLang) {
    return res.status(400).json({ error: 'targetLang is required' });
  }
  if (sourceLang === targetLang) {
    return res.status(400).json({
      error: 'sourceLang and targetLang must be different'
    });
  }

  const validLangs = ['hi', 'bn', 'ta', 'te', 'mr'];
  if (!validLangs.includes(sourceLang)) {
    return res.status(400).json({
      error: `Invalid sourceLang. Must be one of: ${validLangs.join(', ')}`
    });
  }
  if (!validLangs.includes(targetLang)) {
    return res.status(400).json({
      error: `Invalid targetLang. Must be one of: ${validLangs.join(', ')}`
    });
  }

  console.log(`\n🎙️  Translate request: ${sourceLang} → ${targetLang}`);
  console.log(`   Audio file: ${audioFile.filename} (${audioFile.size} bytes)`);
  if (patientName) console.log(`   Patient: ${patientName}`);

  try {
    // ── STEP 1: ASR — audio file → text ─────────────────────────────────
    console.log('   [1/3] Running ASR...');
    const asrResult = await mlService.runASR(audioFile.path, sourceLang);

    if (!asrResult.text || asrResult.text.trim() === '') {
      return res.status(422).json({
        error: 'ASR returned empty text. Audio may be too short or silent.'
      });
    }
    console.log(`   ✅ ASR done in ${asrResult.latencyMs}ms: "${asrResult.text}"`);

    // ── STEP 2: NMT — source text → translated text ──────────────────────
    console.log('   [2/3] Running NMT...');
    const nmtResult = await mlService.runNMT(
      asrResult.text,
      sourceLang,
      targetLang
    );

    if (!nmtResult.translatedText || nmtResult.translatedText.trim() === '') {
      return res.status(422).json({
        error: 'Translation returned empty result.'
      });
    }
    console.log(`   ✅ NMT done in ${nmtResult.latencyMs}ms: "${nmtResult.translatedText}"`);

    // ── STEP 3: TTS — translated text → audio file ───────────────────────
    console.log('   [3/3] Running TTS...');
    const ttsResult = await mlService.runTTS(nmtResult.translatedText, targetLang);
    console.log(`   ✅ TTS done in ${ttsResult.latencyMs}ms`);

    // ── STEP 4: Save to DB ───────────────────────────────────────────────
    const record = await prisma.healthRecord.create({
      data: {
        originalText:   asrResult.text,
        translatedText: nmtResult.translatedText,
        sourceLang,
        targetLang,
        audioInputUrl:  audioFile.path,
        audioOutputUrl: ttsResult.audioPath,
        patientName:    patientName?.trim() || null,
      },
    });
    console.log(`   💾 Saved record: ${record.id}`);

    // ── STEP 5: Respond ─────────────────────────────────────────────────
    const totalMs = asrResult.latencyMs + nmtResult.latencyMs + ttsResult.latencyMs;
    console.log(`   🏁 Done in ${totalMs}ms total\n`);

    return res.json({
      success: true,
      recordId:       record.id,
      originalText:   asrResult.text,
      translatedText: nmtResult.translatedText,
      audioUrl:       `/audio/${path.basename(ttsResult.audioPath)}`,
      latencyMs:      totalMs,
    });

  } catch (err) {
    console.error('❌ Translation pipeline error:', err.message);

    // Clean up uploaded audio file if pipeline failed
    // No point keeping a file whose record was never saved
    if (audioFile?.path && fs.existsSync(audioFile.path)) {
      fs.unlinkSync(audioFile.path);
    }

    return res.status(500).json({
      error: 'Translation pipeline failed',
      detail: err.message,
    });
  }
};