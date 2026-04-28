'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from '../styles/Navbar.module.css';

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className={styles.navbar}>
      <div className={`container ${styles.inner}`}>

        {/* Logo */}
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>🏥</span>
          <span className={styles.logoText}>
            Health<span className={styles.logoAccent}>Voice</span>
          </span>
        </Link>

        {/* Nav Links */}
        <div className={styles.links}>
          <Link
            href="/translate"
            className={`${styles.link} ${pathname === '/translate' ? styles.active : ''}`}
          >
            🎙️ Translate
          </Link>
          <Link
            href="/records"
            className={`${styles.link} ${pathname === '/records' ? styles.active : ''}`}
          >
            📋 Records
          </Link>
        </div>

      </div>
    </nav>
  );
}