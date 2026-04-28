'use client';
import styles from '../styles/MicButton.module.css';

export default function MicButton({ isRecording, isProcessing, onStart, onStop }) {
  return (
    <div className={styles.wrapper}>
      <button
        className={`${styles.btn} ${isRecording ? styles.recording : ''}`}
        onMouseDown={onStart}
        onMouseUp={onStop}
        onTouchStart={onStart}
        onTouchEnd={onStop}
        disabled={isProcessing}
      >
        <span className={styles.icon}>{isRecording ? '⏹️' : '🎙️'}</span>
        <span className={styles.label}>
          {isProcessing
            ? 'Processing...'
            : isRecording
            ? 'Release to Stop'
            : 'Hold to Record'}
        </span>
        {isRecording && <span className={styles.pulse} />}
      </button>
      <p className={styles.hint}>
        {isProcessing
          ? 'Transcribing and translating your speech...'
          : 'Hold the button and speak clearly into your microphone'}
      </p>
    </div>
  );
}