require('dotenv').config();
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const ML_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
const USE_MOCK = process.env.USE_MOCK_ML === 'true';

// ─── MOCK DATA ─────────────────────────────────────────────────────
const MOCK_TRANSCRIPTIONS = {
  hi: 'मुझे कल से बुखार है और सिर में दर्द हो रहा है।',
  bn: 'আমার গতকাল থেকে জ্বর এবং মাথাব্যথা হচ্ছে।',
  ta: 'எனக்கு நேற்றிலிருந்து காய்ச்சல் மற்றும் தலைவலி உள்ளது.',
  te: 'నాకు నిన్నటి నుండి జ్వరం మరియు తలనొప్పి ఉంది.',
  mr: 'मला कालपासून ताप आणि डोकेदुखी आहे.',
};

const MOCK_TRANSLATIONS = {
  hi: 'I have had fever and headache since yesterday.',
  bn: 'I have had fever and headache since yesterday.',
  ta: 'I have had fever and headache since yesterday.',
  te: 'I have had fever and headache since yesterday.',
  mr: 'I have had fever and headache since yesterday.',
};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// ─── ASR ───────────────────────────────────────────────────────────
exports.runASR = async (audioFilePath, lang) => {
  const start = Date.now();

  if (USE_MOCK) {
    await sleep(800);
    return {
      text: MOCK_TRANSCRIPTIONS[lang] || `[mock transcription in ${lang}]`,
      latencyMs: Date.now() - start,
    };
  }

  const form = new FormData();
  form.append('file', fs.createReadStream(audioFilePath));
  form.append('lang', lang);

  const response = await axios.post(`${ML_URL}/asr`, form, {
    headers: form.getHeaders(),
    timeout: 30000,
  });

  return {
    text: response.data.text,
    latencyMs: Date.now() - start,
  };
};

// ─── NMT ───────────────────────────────────────────────────────────
exports.runNMT = async (text, sourceLang, targetLang) => {
  const start = Date.now();

  if (USE_MOCK) {
    await sleep(400);
    return {
      translatedText: MOCK_TRANSLATIONS[sourceLang]
        || `[mock translation: ${text} → ${targetLang}]`,
      latencyMs: Date.now() - start,
    };
  }

  const response = await axios.post(`${ML_URL}/translate`, {
    text, sourceLang, targetLang,
  }, { timeout: 15000 });

  return {
    translatedText: response.data.translatedText,
    latencyMs: Date.now() - start,
  };
};

// ─── TTS ───────────────────────────────────────────────────────────
exports.runTTS = async (text, lang) => {
  const start = Date.now();

  if (USE_MOCK) {
    await sleep(600);
    const mockFilename = `tts_${Date.now()}.mp3`;
    const savePath = path.join(
      process.env.UPLOAD_DIR || './uploads',
      mockFilename
    );
    fs.writeFileSync(savePath, Buffer.alloc(0));
    return {
      audioPath: savePath,
      latencyMs: Date.now() - start,
    };
  }

  const response = await axios.post(`${ML_URL}/tts`, {
    text, lang,
  }, { timeout: 15000 });

  const filename = response.data.filename;
  return {
    audioPath: `${ML_URL}/audio/${filename}`,
    latencyMs: Date.now() - start,
  };
};

// ─── HEALTH CHECK ──────────────────────────────────────────────────
exports.checkMLHealth = async () => {
  if (USE_MOCK) return { status: 'mocked', up: true };
  try {
    const r = await axios.get(`${ML_URL}/health`, { timeout: 2000 });
    return { status: 'up', up: true, data: r.data };
  } catch {
    return { status: 'down', up: false };
  }
};