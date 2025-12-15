"use client";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { ApiClient, ProviderDTO } from "@menna/shared";
import { useLocale } from "../../locale-context";

export default function ProviderProfile() {
  const params = useParams<{ id: string }>();
  const [provider, setProvider] = useState<ProviderDTO | null>(null);
  const { locale, strings, dir } = useLocale();
  const client = useMemo(() => new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000", locale), [locale]);

  useEffect(() => {
    if (params?.id) {
      client.getProvider(Number(params.id)).then(setProvider);
    }
  }, [params?.id]);

  if (!provider) return <div className="page">...جاري التحميل</div>;

  return (
    <div className={`page card provider-card ${dir}`}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h1>{provider.name}</h1>
          {provider.verified && <span className="badge">منّا موثوق</span>}
        </div>
        <div>{provider.rating.toFixed(1)} ★</div>
      </div>
      <p>{provider.bio_i18n[locale] || provider.bio_i18n["en"]}</p>
      <p>اللغات: {provider.languages.join(", ")}</p>
      <div style={{ display: "flex", gap: 10 }}>
        <a className="cta primary" href={`https://wa.me/${provider.whatsapp || ""}`}>{strings.ctas.whatsapp}</a>
        <a className="cta secondary" style={{ background: "#f28705" }} href={`tel:${provider.phone || ""}`}>{strings.ctas.call}</a>
      </div>
    </div>
  );
}
