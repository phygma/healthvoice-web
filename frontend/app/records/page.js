'use client';
import { useState, useEffect } from 'react';
import styles from './records.module.css';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';

const LANG_NAMES = {
  hi: 'Hindi', bn: 'Bengali',
  ta: 'Tamil', te: 'Telugu', mr: 'Marathi',
};

export default function RecordsPage() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleting, setDeleting] = useState(null);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${BACKEND_URL}/api/records`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to fetch');
      setRecords(data.records);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this record? This cannot be undone.')) return;
    setDeleting(id);
    try {
      const res = await fetch(`${BACKEND_URL}/api/records/${id}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Delete failed');
      setRecords(prev => prev.filter(r => r.id !== id));
    } catch (err) {
      alert('Failed to delete: ' + err.message);
    } finally {
      setDeleting(null);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleString('en-IN', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  };

  const getUrgencyClass = (urgency) => {
    const map = {
      low: 'badge-success',
      moderate: 'badge-warning',
      high: 'badge-danger',
      emergency: 'badge-danger',
    };
    return map[urgency] || 'badge-primary';
  };

  return (
    <div className={styles.page}>
      <div className="container">

        {/* Header */}
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Health Records</h1>
            <p className={styles.subtitle}>
              All past translation and diagnosis sessions
            </p>
          </div>
          <div className={styles.headerRight}>
            <span className={styles.count}>
              {records.length} record{records.length !== 1 ? 's' : ''}
            </span>
            <button
              className="btn btn-outline btn-sm"
              onClick={fetchRecords}
              disabled={loading}
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className={styles.centered}>
            <span className="spinner spinner-dark"
              style={{ width: 36, height: 36, borderWidth: 3 }} />
            <p>Loading records...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className={styles.error}>
            ⚠️ {error}
            <button className="btn btn-sm btn-outline"
              onClick={fetchRecords}>Retry</button>
          </div>
        )}

        {/* Empty */}
        {!loading && !error && records.length === 0 && (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>📋</div>
            <h3>No records yet</h3>
            <p>Translated sessions will appear here</p>
            <a href="/translate" className="btn btn-primary">
              🎙️ Start Translating
            </a>
          </div>
        )}

        {/* Records List */}
        {!loading && records.length > 0 && (
          <div className={styles.list}>
            {records.map(record => (
              <div key={record.id} className={styles.card}>

                {/* Card Header */}
                <div className={styles.cardHeader}>
                  <div className={styles.cardMeta}>
                    <span className={styles.patientName}>
                      👤 {record.patientName || 'Unknown Patient'}
                    </span>
                    <span className={styles.langPair}>
                      {LANG_NAMES[record.sourceLang]} →{' '}
                      {LANG_NAMES[record.targetLang]}
                    </span>
                    <span className={styles.date}>
                      🕒 {formatDate(record.createdAt)}
                    </span>
                  </div>
                  <div className={styles.cardActions}>
                    <button
                      className="btn btn-sm btn-outline"
                      onClick={() =>
                        setExpandedId(
                          expandedId === record.id ? null : record.id
                        )
                      }
                    >
                      {expandedId === record.id ? '▲ Less' : '▼ More'}
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(record.id)}
                      disabled={deleting === record.id}
                    >
                      {deleting === record.id
                        ? <span className="spinner" />
                        : '🗑️'}
                    </button>
                  </div>
                </div>

                {/* Text Preview */}
                <div className={styles.textRow}>
                  <div className={styles.textBox}>
                    <p className={styles.textLabel}>Original</p>
                    <p className={styles.textContent}>
                      {record.originalText}
                    </p>
                  </div>
                  <div className={styles.textArrow}>→</div>
                  <div className={styles.textBox}>
                    <p className={styles.textLabel}>Translation</p>
                    <p className={styles.textContent}>
                      {record.translatedText}
                    </p>
                  </div>
                </div>

                {/* Expanded — Diagnosis */}
                {expandedId === record.id && record.diagnosis && (
                  <div className={styles.diagnosisSection}>
                    <h4 className={styles.diagnosisTitle}>
                      🩺 AI Diagnosis
                    </h4>
                    <div className={styles.diagnosisGrid}>
                      <div className={styles.diagnosisItem}>
                        <span className={styles.diagnosisLabel}>
                          Predicted Disease
                        </span>
                        <span className={styles.diagnosisValue}>
                          {record.diagnosis.predictedDisease ||
                            record.diagnosis.possibleConditions?.[0]?.name}
                        </span>
                      </div>
                      <div className={styles.diagnosisItem}>
                        <span className={styles.diagnosisLabel}>
                          Confidence
                        </span>
                        <span className={styles.diagnosisValue}>
                          {record.diagnosis.confidence
                            ? `${(record.diagnosis.confidence * 100).toFixed(0)}%`
                            : record.diagnosis.possibleConditions?.[0]?.confidence}
                        </span>
                      </div>
                      <div className={styles.diagnosisItem}>
                        <span className={styles.diagnosisLabel}>
                          Specialist
                        </span>
                        <span className={styles.diagnosisValue}>
                          {record.diagnosis.recommendedSpecialist}
                        </span>
                      </div>
                      <div className={styles.diagnosisItem}>
                        <span className={styles.diagnosisLabel}>
                          Urgency
                        </span>
                        <span className={`badge ${getUrgencyClass(record.diagnosis.urgency)}`}>
                          {record.diagnosis.urgency}
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {expandedId === record.id && !record.diagnosis && (
                  <div className={styles.noDiagnosis}>
                    No diagnosis run for this record.
                    <a href="/translate">Run a new translation</a> to get diagnosis.
                  </div>
                )}

              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
}