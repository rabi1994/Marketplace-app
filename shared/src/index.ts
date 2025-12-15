import { z } from "zod";

export const i18nString = z.record(z.string(), z.string());

export const ProviderSchema = z.object({
  id: z.number().optional(),
  name: z.string(),
  bio_i18n: i18nString,
  avatar_url: z.string().optional(),
  verified: z.boolean().default(false),
  languages: z.array(z.string()),
  categories: z.array(z.number()),
  city_id: z.number(),
  area_ids: z.array(z.number()),
  pricing_hint: z.string().optional(),
  availability: z.string().optional(),
  whatsapp: z.string().optional(),
  phone: z.string().optional(),
  rating: z.number().default(0),
  rating_count: z.number().default(0)
});

export const LeadRequestSchema = z.object({
  category_id: z.number(),
  city_id: z.number(),
  area_ids: z.array(z.number()),
  description: z.string(),
  preferred_time: z.string().optional()
});

export const ReviewSchema = z.object({
  lead_id: z.number(),
  provider_id: z.number(),
  rating: z.number().min(1).max(5),
  comment: z.string().optional()
});

export type ProviderDTO = z.infer<typeof ProviderSchema>;
export type LeadRequestDTO = z.infer<typeof LeadRequestSchema>;
export type ReviewDTO = z.infer<typeof ReviewSchema>;

export type Locale = "ar" | "he" | "en";

export class ApiClient {
  constructor(private baseUrl: string, private locale: Locale = "ar", private token?: string) {}

  private headers() {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "Accept-Language": this.locale
    };
    if (this.token) headers["Authorization"] = `Bearer ${this.token}`;
    return headers;
  }

  async listProviders(params: Record<string, string | number | boolean | undefined> = {}): Promise<ProviderDTO[]> {
    const url = new URL("/providers", this.baseUrl);
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) url.searchParams.append(key, String(value));
    });
    const res = await fetch(url, { headers: this.headers() });
    if (!res.ok) throw new Error("Failed to fetch providers");
    return ProviderSchema.array().parse(await res.json());
  }

  async getProvider(id: number): Promise<ProviderDTO> {
    const res = await fetch(`${this.baseUrl}/providers/${id}`, { headers: this.headers() });
    if (!res.ok) throw new Error("Provider not found");
    return ProviderSchema.parse(await res.json());
  }

  async createLead(payload: LeadRequestDTO): Promise<{ id: number }> {
    const res = await fetch(`${this.baseUrl}/leads`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to create lead");
    return res.json();
  }

  async createReview(payload: ReviewDTO) {
    const res = await fetch(`${this.baseUrl}/reviews`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to create review");
    return res.json();
  }
}
