// This service is the ONLY file that talks to the Python ML service.
// All ML calls go through here.
//
// MOCK MODE: When USE_MOCK_ML=true in .env, returns fake data instantly
// instead of calling the real Python service. This lets the backend be
// fully functional before the ML service is ready.

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const ML_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
const USE_MOCK = process.env.USE_MOCK_ML === 'true';

// ─── MOCK DATA ────────────────────────────────────────────────────────────
// Realistic-looking transcriptions for each language so the UI looks plausible.
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

// Helper: simulate network delay so frontend loading states are visible
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// ─── ASR ──────────────────────────────────────────────────────────────────
// Calls Python /asr endpoint OR returns mock data
// Returns: { text: string, latencyMs: number }
exports.runASR = async (audioFilePath, lang) => {
  const start = Date.now();

  if (USE_MOCK) {
    await sleep(800); // pretend Whisper took 800ms
    return {
      text: MOCK_TRANSCRIPTIONS[lang] || `[mock transcription in ${lang}]`,
      latencyMs: Date.now() - start,
    };
  }

  const form = new FormData();
  form.append('audio', fs.createReadStream(audioFilePath));
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

// ─── NMT ──────────────────────────────────────────────────────────────────
// Calls Python /translate endpoint OR returns mock data
// Returns: { translatedText: string, latencyMs: number }
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

// ─── TTS ──────────────────────────────────────────────────────────────────
// Calls Python /tts endpoint OR creates a placeholder mp3
// Returns: { audioPath: string, latencyMs: number }
exports.runTTS = async (text, lang) => {
  const start = Date.now();
  const filename = `tts_${Date.now()}.mp3`;
  const savePath = path.join(process.env.UPLOAD_DIR || './uploads', filename);

  if (USE_MOCK) {
    await sleep(600);
    // Create an empty placeholder file so the audio URL points to something real.
    // Frontend will get a 200 response but the audio won't play (silent file).
    // That's fine for backend dev — frontend can mock-play with a beep if needed.
    fs.writeFileSync(savePath, Buffer.alloc(0));
    return {
      audioPath: savePath,
      latencyMs: Date.now() - start,
    };
  }

  await axios.post(`${ML_URL}/tts`, {
    text, lang, outputPath: savePath,
  }, { timeout: 15000 });

  return {
    audioPath: savePath,
    latencyMs: Date.now() - start,
  };
};

// ─── HEALTH CHECK ────────────────────────────────────────────────────────
// Used by /api/health to know if real ML is reachable
exports.checkMLHealth = async () => {
  if (USE_MOCK) return { status: 'mocked', up: true };
  try {
    const r = await axios.get(`${ML_URL}/health`, { timeout: 2000 });
    return { status: 'up', up: true, data: r.data };
  } catch {
    return { status: 'down', up: false };
  }
};