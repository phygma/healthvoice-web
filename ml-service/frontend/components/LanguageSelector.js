import styles from '../styles/LanguageSelector.module.css';
import { LANGUAGES } from '../utils/languages';

export default function LanguageSelector({ label, value, onChange, exclude }) {
  return (
    <div className={styles.wrapper}>
      <label className={styles.label}>{label}</label>
      <select
        className={styles.select}
        value={value}
        onChange={e => onChange(e.target.value)}
      >
        {LANGUAGES.filter(l => l.code !== exclude).map(lang => (
          <option key={lang.code} value={lang.code}>
            {lang.name} ({lang.native})
          </option>
        ))}
      </select>
    </div>
  );
}