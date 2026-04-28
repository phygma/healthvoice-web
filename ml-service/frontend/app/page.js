import Link from 'next/link';
import styles from './page.module.css';

export default function HomePage() {
  return (
    <div className={styles.page}>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className="container">
          <div className={styles.heroContent}>

            <div className={styles.badge}>
              <span className="badge badge-primary">
                🇮🇳 Built for India
              </span>
            </div>

            <h1 className={styles.title}>
              Breaking Language Barriers
              <br />
              <span className="gradient-text">in Healthcare</span>
            </h1>

            <p className={styles.subtitle}>
              Speak in your language, be understood in theirs.
              Real-time voice translation across Hindi, Tamil, Bengali,
              Telugu and Marathi — powered by AI.
            </p>

            <div className={styles.actions}>
              <Link href="/translate" className="btn btn-primary btn-lg">
                🎙️ Start Translating
              </Link>
              <Link href="/records" className="btn btn-outline btn-lg">
                📋 View Records
              </Link>
            </div>

            <div className={styles.stats}>
              <div className={styles.stat}>
                <span className={styles.statNumber}>5</span>
                <span className={styles.statLabel}>Indian Languages</span>
              </div>
              <div className={styles.statDivider} />
              <div className={styles.stat}>
                <span className={styles.statNumber}>41</span>
                <span className={styles.statLabel}>Diseases Detected</span>
              </div>
              <div className={styles.statDivider} />
              <div className={styles.stat}>
                <span className={styles.statNumber}>97%</span>
                <span className={styles.statLabel}>Model Accuracy</span>
              </div>
            </div>

          </div>

          <div className={styles.features}>
            {[
              {
                icon: '🎙️',
                title: 'Voice Recognition',
                desc: 'Whisper AI transcribes speech in any Indian language with high accuracy',
                color: '#6C63FF',
              },
              {
                icon: '🌐',
                title: 'Smart Translation',
                desc: 'Translates between 5 Indian languages instantly using NMT',
                color: '#00BFA6',
              },
              {
                icon: '🔊',
                title: 'Audio Playback',
                desc: 'Converts translated text to natural speech the patient can hear',
                color: '#F59E0B',
              },
              {
                icon: '🩺',
                title: 'AI Diagnosis',
                desc: 'Predicts possible conditions from symptoms using a trained ML model',
                color: '#EF4444',
              },
            ].map((f) => (
              <div key={f.title} className={styles.featureCard}>
                <div
                  className={styles.featureIcon}
                  style={{ background: `${f.color}20`, color: f.color }}
                >
                  {f.icon}
                </div>
                <h3 className={styles.featureTitle}>{f.title}</h3>
                <p className={styles.featureDesc}>{f.desc}</p>
              </div>
            ))}
          </div>

        </div>
      </section>

    </div>
  );
}