// Handles multipart/form-data audio file uploads.
// Uses multer under the hood — saves audio to /uploads with a UUID filename
// so concurrent requests never overwrite each other.

const multer = require('multer');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, process.env.UPLOAD_DIR || './uploads');
  },
  filename: (req, file, cb) => {
    // UUID prevents filename collisions across concurrent requests
    const ext = path.extname(file.originalname) || '.webm';
    cb(null, `audio_${uuidv4()}${ext}`);
  },
});

const fileFilter = (req, file, cb) => {
  // Browser MediaRecorder outputs audio/webm — must accept it
  if (file.mimetype.startsWith('audio/')) {
    cb(null, true);
  } else {
    cb(new Error('Only audio files are accepted'), false);
  }
};

exports.uploadAudio = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: (parseInt(process.env.MAX_AUDIO_SIZE_MB) || 10) * 1024 * 1024,
  },
});