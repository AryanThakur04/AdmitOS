const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API}/api/v1${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  if (res.headers.get("content-type")?.includes("application/pdf")) {
    return res.blob() as unknown as T;
  }
  return res.json();
}

export const demoStats = {
  total_leads: 15,
  hot_leads: 5,
  medium_leads: 6,
  cold_leads: 4,
  active_alerts: 8,
  conversion_rate: 13.3,
  avg_aging_score: 32.4,
  leads_by_source: { facebook: 4, website: 5, whatsapp_referral: 3, csv_import: 2, google_sheets: 1 },
  leads_by_status: { new: 2, contacted: 4, qualified: 3, application: 2, accepted: 2, lost: 2 },
  weekly_new_leads: [1, 2, 0, 3, 2, 1, 4],
};
