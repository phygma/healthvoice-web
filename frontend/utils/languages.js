export const LANGUAGES = [
  { code: 'hi', name: 'Hindi',   native: 'हिंदी'    },
  { code: 'bn', name: 'Bengali', native: 'বাংলা'    },
  { code: 'ta', name: 'Tamil',   native: 'தமிழ்'   },
  { code: 'te', name: 'Telugu',  native: 'తెలుగు'  },
  { code: 'mr', name: 'Marathi', native: 'मराठी'   },
];

export const getLangName = (code) => {
  const lang = LANGUAGES.find(l => l.code === code);
  return lang ? `${lang.name} (${lang.native})` : code;
};