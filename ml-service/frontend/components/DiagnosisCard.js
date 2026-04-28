import styles from '../styles/DiagnosisCard.module.css';

const URGENCY_LABELS = {
  low:       { label: 'Low',       className: 'badge-success' },
  moderate:  { label: 'Moderate',  className: 'badge-warning' },
  high:      { label: 'High',      className: 'badge-danger'  },
  emergency: { label: 'Emergency', className: 'badge-danger'  },
};

export default function DiagnosisCard({ diagnosis }) {
  if (!diagnosis) return null;

  const urgency = URGENCY_LABELS[diagnosis.urgency] || URGENCY_LABELS.low;

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.headerIcon}>🩺</span>
        <h3 className={styles.headerTitle}>AI Diagnosis</h3>
        <span className={`badge ${urgency.className}`}>
          {urgency.label} Urgency
        </span>
      </div>

      {/* Top Prediction */}
      <div className={styles.topPrediction}>
        <div className={styles.diseaseName}>
          {diagnosis.predictedDisease || diagnosis.possibleConditions?.[0]?.name}
        </div>
        <div className={styles.confidence}>
          {diagnosis.confidence
            ? `${(diagnosis.confidence * 100).toFixed(0)}% confidence`
            : diagnosis.possibleConditions?.[0]?.confidence}
        </div>
      </div>

      {/* All Conditions */}
      {(diagnosis.topConditions || diagnosis.possibleConditions) && (
        <div className={styles.conditions}>
          <p className={styles.sectionLabel}>Possible Conditions</p>
          {(diagnosis.topConditions || diagnosis.possibleConditions).map((c, i) => (
            <div key={i} className={styles.condition}>
              <span className={styles.conditionName}>
                {c.disease || c.name}
              </span>
              <span className={styles.conditionProb}>
                {c.probability
                  ? `${(c.probability * 100).toFixed(0)}%`
                  : c.confidence}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Detected Symptoms */}
      {diagnosis.detectedSymptoms?.length > 0 && (
        <div className={styles.symptoms}>
          <p className={styles.sectionLabel}>Detected Symptoms</p>
          <div className={styles.symptomTags}>
            {diagnosis.detectedSymptoms.map((s, i) => (
              <span key={i} className={styles.symptomTag}>{s}</span>
            ))}
          </div>
        </div>
      )}

      {/* Specialist */}
      <div className={styles.specialist}>
        <span className={styles.specialistIcon}>👨‍⚕️</span>
        <div>
          <p className={styles.specialistLabel}>Recommended Specialist</p>
          <p className={styles.specialistName}>{diagnosis.recommendedSpecialist}</p>
        </div>
      </div>

      {/* Disclaimer */}
      <p className={styles.disclaimer}>{diagnosis.disclaimer}</p>
    </div>
  );
}