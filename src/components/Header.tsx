import type { ReactNode } from "react";
import locales from "../content/locales.json";

type Language = keyof typeof locales;
type IconName = "arrow" | "chevron" | "menu";
const paths: Record<IconName, string> = {
  arrow: "M7 17 17 7M7 7h10v10",
  chevron: "m8 10 4 4 4-4",
  menu: "M4 7h16M4 12h16M4 17h16",
};
function Icon({ name }: { name: IconName }) {
  return <svg className="icon" viewBox="0 0 24 24" aria-hidden="true"><path d={paths[name]} /></svg>;
}
export function BrandMark() {
  return <svg className="brand-mark" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M5 5h16v16H5zM15 15h16v16H15z" stroke="currentColor" strokeWidth="3.5"/><path d="M15 15h6v6h-6z" fill="currentColor"/></svg>;
}
function NavigationLinks({ lang }: { lang: Language }) {
  const copy = locales[lang];
  return <><a href="#proyectos">{copy.projects}</a><a href="#servicios">{copy.services}</a><a href="#equipo">{copy.about}</a></>;
}
function ContactButton({ children }: { children: ReactNode }) {
  return <button className="button primary" data-contact>{children}<Icon name="arrow" /></button>;
}
/** Build-time React rendering only. No client directive, hydration, or React browser bundle. */
export default function Header({ lang }: { lang: Language }) {
  const copy = locales[lang];
  return <>
    <a className="skip-link" href="#main">{copy.skip}</a>
    <header className="site-header" id="top">
      <div className="container header-inner">
        <a className="brand" href={copy.home} aria-label={`InsideLabs — ${copy.homeLabel}`}><BrandMark /><span>Inside<span className="brand-labs">Labs</span></span></a>
        <nav className="desktop-nav" aria-label={copy.navLabel}><NavigationLinks lang={lang}/></nav>
        <div className="header-actions">
          <details className="language-switch">
            <summary aria-label={copy.language}><img className="flag" src={lang === "es" ? "/images/flag-cl.svg" : "/images/flag-gb.svg"} width={20} height={14} alt="" aria-hidden="true"/>{lang.toUpperCase()}<Icon name="chevron"/></summary>
            <div className="language-options">
              <a href="/" lang="es" aria-current={lang === "es" ? "page" : undefined}><img className="flag" src="/images/flag-cl.svg" width={20} height={14} alt="" aria-hidden="true"/>Español</a>
              <a href="/en" lang="en" aria-current={lang === "en" ? "page" : undefined}><img className="flag" src="/images/flag-gb.svg" width={20} height={14} alt="" aria-hidden="true"/>English</a>
            </div>
          </details>
          <ContactButton>{copy.talk}</ContactButton>
          <button className="menu-toggle" aria-label={copy.open} aria-expanded="false" aria-controls="mobile-nav"><Icon name="menu"/></button>
        </div>
        <nav className="mobile-nav" id="mobile-nav" aria-label={copy.mobileLabel} hidden><NavigationLinks lang={lang}/><a href="#faq">FAQ</a><ContactButton>{copy.talkLong}</ContactButton></nav>
      </div>
    </header>
  </>;
}
