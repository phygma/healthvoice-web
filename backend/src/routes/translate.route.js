const router = require('express').Router();
const { handleTranslate } = require('../controllers/translate.controller');
const { uploadAudio } = require('../middleware/upload.middleware');

// POST /api/translate
// Body: multipart/form-data
//   audio       : audio file (webm/wav/mp3)
//   sourceLang  : "hi" | "bn" | "ta" | "te" | "mr"
//   targetLang  : "hi" | "bn" | "ta" | "te" | "mr"
//   patientName : string (optional)
router.post('/', uploadAudio.single('audio'), handleTranslate);

module.exports = router;