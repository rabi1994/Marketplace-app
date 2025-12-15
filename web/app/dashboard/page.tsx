"use client";
import { useEffect, useState } from "react";
import { ApiClient, LeadRequestDTO } from "@menna/shared";

export default function DashboardPage() {
  const client = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000");
  const [leads, setLeads] = useState<LeadRequestDTO[]>([]);

  useEffect(() => {
    // Placeholder: in production fetch provider inbox
    setLeads([
      { category_id: 1, city_id: 1, area_ids: [1], description: "تصليح ماس كهربائي", preferred_time: "اليوم" }
    ]);
  }, []);

  return (
    <div className="page">
      <h1>لوحة المزود</h1>
      <div className="grid">
        {leads.map((lead, idx) => (
          <article className="card" key={idx}>
            <p>{lead.description}</p>
            <small>مدينة: {lead.city_id} | فئة: {lead.category_id}</small>
            <button className="cta">قبول وتسليم</button>
          </article>
        ))}
      </div>
    </div>
  );
}
