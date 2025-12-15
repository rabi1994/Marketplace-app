"use client";
import { createContext, useContext, useMemo, useState } from "react";

type Locale = "ar" | "he" | "en";

const stringsByLocale: Record<Locale, any> = {
  ar: {
    tagline: "واحد منّا، ثقة محلية",
    footer: "منّا | ثقة المجتمع المحلي في إسرائيل",
    nav: { home: "الرئيسية", providers: "المحترفون", request: "أطلب خدمة", dashboard: "لوحة المزود", login: "الدخول" },
    hero: {
      title: "خدمة محلية بثقة المجتمع",
      subtitle: "كهربائي، سبّاك، نظافة، تنسيق حدائق وأكثر — بالعربية أولاً مع دعم عبري وإنجليزي.",
      ctaPrimary: "أطلب خدمة الآن",
      ctaSecondary: "تصفح المحترفين"
    },
    filters: { verified: "موثوق فقط" },
    ctas: { whatsapp: "واتساب", call: "اتصال", view: "عرض الملف" },
    rating: "تقييم"
  },
  he: {
    tagline: "אחד מאיתנו, אמון מקומי",
    footer: "מנא | אמון הקהילה בישראל",
    nav: { home: "דף הבית", providers: "בעלי מקצוע", request: "בקש שירות", dashboard: "דאשבורד ספק", login: "התחברות" },
    hero: {
      title: "שירות מקומי עם אמון קהילה",
      subtitle: "חשמלאי, אינסטלטור, ניקיון ועוד — ערבית תחילה עם עברית ואנגלית.",
      ctaPrimary: "בקש שירות עכשיו",
      ctaSecondary: "עיין במקצוענים"
    },
    filters: { verified: "מאומת בלבד" },
    ctas: { whatsapp: "וואטסאפ", call: "שיחה", view: "צפה בפרופיל" },
    rating: "דירוג"
  },
  en: {
    tagline: "One of us, local trust",
    footer: "Menna | Trusted local community in Israel",
    nav: { home: "Home", providers: "Professionals", request: "Request", dashboard: "Provider Dashboard", login: "Login" },
    hero: {
      title: "Local service, community trust",
      subtitle: "Electricians, plumbers, cleaners, gardeners and more — Arabic first with Hebrew & English.",
      ctaPrimary: "Request service now",
      ctaSecondary: "Browse providers"
    },
    filters: { verified: "Verified only" },
    ctas: { whatsapp: "WhatsApp", call: "Call", view: "View profile" },
    rating: "Rating"
  }
};

type LocaleContextValue = {
  locale: Locale;
  setLocale: (loc: Locale) => void;
  dir: "rtl" | "ltr";
  strings: any;
};

const LocaleContext = createContext<LocaleContextValue | null>(null);

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>("ar");
  const dir = locale === "en" ? "ltr" : "rtl";
  const value = useMemo<LocaleContextValue>(
    () => ({ locale, setLocale, dir, strings: stringsByLocale[locale] }),
    [locale]
  );
  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error("LocaleContext not found");
  return ctx;
}
