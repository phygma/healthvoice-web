import './globals.css';
import Navbar from '../components/Navbar';

export const metadata = {
  title: 'HealthVoice — Medical Translation for India',
  description: 'Real-time voice translation across Indian languages for rural healthcare',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  );
}