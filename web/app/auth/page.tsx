"use client";
import { useState } from "react";
import { ApiClient } from "@menna/shared";
import { useLocale } from "../locale-context";

export default function AuthPage() {
  const { locale, strings } = useLocale();
  const client = new ApiClient(process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000", locale);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const login = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      setMessage("تم تسجيل الدخول!");
    } else {
      setMessage("خطأ في البيانات");
    }
  };

  return (
    <div className="page card">
      <h1>{strings.nav.login}</h1>
      <input placeholder="البريد الإلكتروني" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="كلمة السر" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="cta primary" onClick={login}>دخول</button>
      {message && <p>{message}</p>}
    </div>
  );
}
