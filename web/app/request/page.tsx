"use client";
import { useState } from "react";
import { ApiClient } from "@menna/shared";
import { useLocale } from "../locale-context";

export default function RequestPage() {
  const { locale } = useLocale();
  const client = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000", locale);
  const [status, setStatus] = useState<string | null>(null);
  const [form, setForm] = useState({
    category_id: 1,
    city_id: 1,
    area_ids: "1",
    description: ""
  });

  const submit = async () => {
    try {
      const payload = {
        ...form,
        area_ids: form.area_ids.split(",").map((n) => Number(n.trim())),
        category_id: Number(form.category_id),
        city_id: Number(form.city_id)
      };
      await client.createLead(payload);
      setStatus("تم إرسال طلبك إلى أفضل ٣ مزودين.");
    } catch (e: any) {
      setStatus("تعذر إرسال الطلب");
    }
  };

  return (
    <div className="page card">
      <h1>أطلب خدمة</h1>
      <label>الفئة</label>
      <input value={form.category_id} onChange={(e) => setForm({ ...form, category_id: Number(e.target.value) })} />
      <label>المدينة</label>
      <input value={form.city_id} onChange={(e) => setForm({ ...form, city_id: Number(e.target.value) })} />
      <label>المناطق (مفصولة بفاصلة)</label>
      <input value={form.area_ids} onChange={(e) => setForm({ ...form, area_ids: e.target.value })} />
      <label>وصف الطلب</label>
      <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
      <button className="cta" onClick={submit}>إرسال الطلب</button>
      {status && <p>{status}</p>}
    </div>
  );
}
