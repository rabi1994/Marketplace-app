"use client";
import "./globals.css";
import { LocaleProvider, useLocale } from "./locale-context";

function Shell({ children }: { children: React.ReactNode }) {
  const { locale, setLocale, dir, strings } = useLocale();

  return (
    <html lang={locale} dir={dir}>
      <body className={`app ${dir}`}>
        <div className="bg-texture" />
        <header className="topbar glass">
          <div className="brand">
            <span className="logo">منّا | Menna</span>
            <small>{strings.tagline}</small>
          </div>
          <nav className="nav">
            <a href="/">{strings.nav.home}</a>
            <a href="/providers">{strings.nav.providers}</a>
            <a href="/request">{strings.nav.request}</a>
            <a href="/dashboard">{strings.nav.dashboard}</a>
          </nav>
          <div className="actions">
            <select value={locale} onChange={(e) => setLocale(e.target.value as any)}>
              <option value="ar">العربية</option>
              <option value="he">עברית</option>
              <option value="en">English</option>
            </select>
            <a className="cta primary" href="/auth">{strings.nav.login}</a>
          </div>
        </header>
        <main className="page">{children}</main>
        <footer className="footer glass">{strings.footer}</footer>
      </body>
    </html>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <LocaleProvider>
      <Shell>{children}</Shell>
    </LocaleProvider>
  );
}
