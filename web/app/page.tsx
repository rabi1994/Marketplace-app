"use client";
import { useEffect, useState } from "react";
import { ApiClient, ProviderDTO } from "@menna/shared";
import { useLocale } from "./locale-context";

const fallbackProviders: ProviderDTO[] = [
  {
    id: 1,
    name: "حسن | كهربائي تل أبيب",
    bio_i18n: { ar: "خبير شبكات مع سرعة استجابة", he: "חשמלאי מהיר בתל אביב", en: "Fast-response electrician in Tel Aviv" },
    avatar_url: "",
    verified: true,
    languages: ["ar", "he", "en"],
    categories: [1],
    city_id: 1,
    area_ids: [1],
    pricing_hint: "زيارة 180 ₪",
    availability: "اليوم",
    whatsapp: "+972501234567",
    phone: "+972501234567",
    rating: 4.9,
    rating_count: 120
  },
  {
    id: 2,
    name: "نورا | تنظيف من حيفا",
    bio_i18n: { ar: "تنظيف عائلي وشركات صغيرة", he: "ניקיון למשפחות ועסקים קטנים", en: "Home & small business cleaning" },
    avatar_url: "",
    verified: true,
    languages: ["ar", "he"],
    categories: [3],
    city_id: 2,
    area_ids: [3],
    pricing_hint: "120 ₪ للزيارة",
    availability: "غداً",
    whatsapp: "+972541234567",
    phone: "+972541234567",
    rating: 4.8,
    rating_count: 44
  },
  {
    id: 3,
    name: "داني | سبّاك القدس",
    bio_i18n: { ar: "تصليحات طارئة ومياه ساخنة", he: "אינסטלטור חירום ומים חמים", en: "Emergency plumber & boilers" },
    avatar_url: "",
    verified: false,
    languages: ["he", "en"],
    categories: [2],
    city_id: 3,
    area_ids: [4],
    pricing_hint: "150 ₪ للطوارئ",
    availability: "اليوم",
    whatsapp: "+972521234567",
    phone: "+972521234567",
    rating: 4.5,
    rating_count: 31
  }
];

export default function HomePage() {
  const { locale, strings } = useLocale();
  const [providers, setProviders] = useState<ProviderDTO[]>([]);
  const client = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000", locale);

  useEffect(() => {
    client
      .listProviders()
      .then(setProviders)
      .catch(() => setProviders(fallbackProviders));
  }, [locale]);

  return (
    <div className="page">
      <section className="hero">
        <div className="pill">منّا موثوق | Local Verified</div>
        <h1>{strings.hero.title}</h1>
        <p className="subtitle">{strings.hero.subtitle}</p>
        <div className="hero-actions">
          <a className="cta primary" href="/request">
            {strings.hero.ctaPrimary}
          </a>
          <a className="cta secondary" href="/providers">
            {strings.hero.ctaSecondary}
          </a>
        </div>
        <div className="chips">
          <span className="chip">كهربائي</span>
          <span className="chip">سبّاك</span>
          <span className="chip">نظافة</span>
          <span className="chip">حدائق</span>
          <span className="chip">تكييف</span>
        </div>
      </section>

      <section>
        <div className="section-head">
          <div>
            <h2>محترفون مميزون</h2>
            <p className="muted">محليون، موثوقون، يتحدثون لغتك</p>
          </div>
          <a className="cta ghost" href="/providers">{strings.hero.ctaSecondary}</a>
        </div>
        <div className="grid">
          {providers.map((p) => (
            <article className="card provider-card" key={p.id}>
              <div className="provider-top">
                <div>
                  <strong>{p.name}</strong>
                  {p.verified && <span className="badge">منّا موثوق</span>}
                </div>
                <span>{strings.rating}: {p.rating.toFixed(1)} ★</span>
              </div>
              <p>{p.bio_i18n[locale] || p.bio_i18n["en"]}</p>
              <div className="tags">
                <span className="chip small">{p.pricing_hint}</span>
                <span className="chip small">{p.availability}</span>
                <span className="chip small">{p.languages.join(" / ")}</span>
              </div>
              <div className="provider-actions">
                <a className="cta primary" href={`https://wa.me/${p.whatsapp || ""}`}>{strings.ctas.whatsapp}</a>
                <a className="cta secondary" href={`/providers/${p.id}`}>{strings.ctas.view}</a>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
