'use client';
import { useState, useEffect } from 'react';
import LanguageSelector from '../../components/LanguageSelector';
import MicButton from '../../components/MicButton';
import DiagnosisCard from '../../components/DiagnosisCard';
import useAudioRecorder from '../../hooks/useAudioRecorder';
import styles from './translate.module.css';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';

export default function TranslatePage() {
  const [sourceLang, setSourceLang] = useState('hi');
  const [targetLang, setTargetLang] = useState('ta');
  const [patientName, setPatientName] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState('idle');

  const {
    isRecording,
    audioBlob,
    error: micError,
    startRecording,
    stopRecording,
    reset,
  } = useAudioRecorder();

  // ── Auto-submit when audioBlob is ready ──────────────────────────
  useEffect(() => {
    if (audioBlob) {
      handleSubmit(audioBlob);
    }
  }, [audioBlob]);

  const handleSubmit = async (blob) => {
    if (!blob) return;
    setIsProcessing(true);
    setError(null);
    setResult(null);
    setDiagnosis(null);
    setStep('transcribing');

    try {
      const formData = new FormData();
      formData.append('audio', blob, 'recording.webm');
      formData.append('sourceLang', sourceLang);
      formData.append('targetLang', targetLang);
      if (patientName.trim()) {
        formData.append('patientName', patientName.trim());
      }

      setStep('translating');

      const res = await fetch(`${BACKEND_URL}/api/translate`, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.error || 'Translation failed');

      setResult(data);
      setStep('done');

    } catch (err) {
      setError(err.message);
      setStep('idle');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGetDiagnosis = async () => {
    if (!result) return;
    setIsDiagnosing(true);
    setDiagnosis(null);

    try {
      const res = await fetch(`${BACKEND_URL}/api/diagnose`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symptomText: result.originalText,
          sourceLang,
          recordId: result.recordId,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Diagnosis failed');
      setDiagnosis(data.diagnosis);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsDiagnosing(false);
    }
  };

  const handleReset = () => {
    reset();
    setResult(null);
    setDiagnosis(null);
    setError(null);
    setStep('idle');
    setPatientName('');
  };

  return (
    <div className={styles.page}>
      <div className="container">

        <div className={styles.header}>
          <h1 className={styles.title}>Voice Translator</h1>
          <p className={styles.subtitle}>
            Record a patient's symptoms and translate them instantly
          </p>
        </div>

        <div className={styles.layout}>

          {/* Left Panel — Controls */}
          <div className={styles.controls}>

            <div className="card">
              <h2 className={styles.cardTitle}>Language Settings</h2>
              <div className={styles.langRow}>
                <LanguageSelector
                  label="Patient speaks"
                  value={sourceLang}
                  onChange={setSourceLang}
                  exclude={targetLang}
                />
                <div className={styles.arrow}>→</div>
                <LanguageSelector
                  label="Translate to"
                  value={targetLang}
                  onChange={setTargetLang}
                  exclude={sourceLang}
                />
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.inputLabel}>
                  Patient Name (optional)
                </label>
                <input
                  type="text"
                  className={styles.input}
                  placeholder="Enter patient name..."
                  value={patientName}
                  onChange={e => setPatientName(e.target.value)}
                  disabled={isProcessing || isRecording}
                />
              </div>
            </div>

            <div className={`card ${styles.micCard}`}>
              <MicButton
                isRecording={isRecording}
                isProcessing={isProcessing}
                onStart={startRecording}
                onStop={stopRecording}
              />

              {isProcessing && (
                <div className={styles.processingSteps}>
                  {[
                    { key: 'transcribing', label: 'Transcribing audio...' },
                    { key: 'translating',  label: 'Translating text...'   },
                    { key: 'done',         label: 'Generating audio...'   },
                  ].map((s, i) => (
                    <div
                      key={s.key}
                      className={`${styles.stepItem} ${
                        step === s.key || step === 'done' ||
                        (step === 'translating' && i === 0)
                          ? styles.stepDone : ''
                      }`}
                    >
                      <span>{i + 1}</span> {s.label}
                    </div>
                  ))}
                </div>
              )}

              {(error || micError) && (
                <div className={styles.error}>
                  ⚠️ {error || micError}
                </div>
              )}
            </div>

            {result && (
              <button className="btn btn-outline" onClick={handleReset}>
                🔄 New Recording
              </button>
            )}

          </div>

          {/* Right Panel — Results */}
          <div className={styles.results}>

            {!result && !isProcessing && (
              <div className={styles.empty}>
                <div className={styles.emptyIcon}>🎙️</div>
                <h3>Ready to Record</h3>
                <p>Select languages, then hold the mic button and speak</p>
              </div>
            )}

            {isProcessing && (
              <div className={styles.empty}>
                <div className={styles.emptyIcon}>
                  <span
                    className="spinner spinner-dark"
                    style={{ width: 40, height: 40, borderWidth: 4 }}
                  />
                </div>
                <h3>Processing...</h3>
                <p>Running AI translation pipeline</p>
              </div>
            )}

            {result && (
              <>
                <div className="card">
                  <h3 className={styles.resultLabel}>
                    🗣️ Original ({sourceLang.toUpperCase()})
                  </h3>
                  <p className={styles.resultText}>{result.originalText}</p>
                </div>

                <div className="card">
                  <h3 className={styles.resultLabel}>
                    🌐 Translation ({targetLang.toUpperCase()})
                  </h3>
                  <p className={styles.resultText}>{result.translatedText}</p>
                </div>

                {result.audioUrl && (
                  <div className="card">
                    <h3 className={styles.resultLabel}>🔊 Audio Output</h3>
                    <audio
                      controls
                      src={
                        result.audioUrl.startsWith('http')
                          ? result.audioUrl
                          : `${BACKEND_URL}${result.audioUrl}`
                      }
                      className={styles.audio}
                    />
                  </div>
                )}

                {!diagnosis && (
                  <button
                    className="btn btn-secondary"
                    onClick={handleGetDiagnosis}
                    disabled={isDiagnosing}
                    style={{ width: '100%' }}
                  >
                    {isDiagnosing
                      ? <><span className="spinner" /> Analyzing symptoms...</>
                      : '🩺 Get AI Diagnosis'}
                  </button>
                )}

                {diagnosis && <DiagnosisCard diagnosis={diagnosis} />}

                <p className={styles.latency}>
                  ⚡ Processed in {(result.latencyMs / 1000).toFixed(1)}s
                </p>
              </>
            )}

          </div>
        </div>

      </div>
    </div>
  );
}