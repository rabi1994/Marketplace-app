"use client";
import { useEffect, useMemo, useState } from "react";
import { ApiClient, ProviderDTO } from "@menna/shared";
import { useLocale } from "../locale-context";

export default function ProvidersPage() {
  const { locale, strings, dir } = useLocale();
  const [providers, setProviders] = useState<ProviderDTO[]>([]);
  const [filterVerified, setFilterVerified] = useState(false);
  const client = useMemo(() => new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000", locale), [locale]);

  useEffect(() => {
    client.listProviders({ verified: filterVerified || undefined }).then(setProviders);
  }, [filterVerified, locale]);

  return (
    <div className={`page ${dir}`}>
      <div className="section-head">
        <div>
          <h1>{strings.nav.providers}</h1>
          <p className="muted">اختر لغة، تقييم، أو موثوقية</p>
        </div>
        <label className="filter-chip">
          <input type="checkbox" checked={filterVerified} onChange={(e) => setFilterVerified(e.target.checked)} /> {strings.filters.verified}
        </label>
      </div>
      <label>
        <input type="checkbox" checked={filterVerified} onChange={(e) => setFilterVerified(e.target.checked)} /> {strings.filters.verified}
      </label>
      <div className="grid" style={{ marginTop: 12 }}>
        {providers.map((p) => (
          <article className="card provider-card" key={p.id}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{p.name}</strong>
                {p.verified && <span className="badge">منّا موثوق</span>}
              </div>
              <span>{p.rating.toFixed(1)} ★</span>
            </div>
            <p>{p.bio_i18n[locale] || p.bio_i18n["en"]}</p>
            <small>اللغات: {p.languages.join(", ")}</small>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <a className="cta secondary" href={`/providers/${p.id}`}>
                {strings.ctas.view}
              </a>
              <a className="cta primary" style={{ background: "#f28705" }} href={`https://wa.me/${p.whatsapp || ""}`}>
                {strings.ctas.whatsapp}
              </a>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
