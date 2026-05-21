import { useEffect, useState } from "react";
import { api } from "../api/client";
import { AlertTriangle } from "lucide-react";

interface Alert {
  id: number;
  lead_id: number;
  type: string;
  message: string;
  severity: string;
}

const demoAlerts: Alert[] = [
  { id: 1, lead_id: 3, type: "no_reply_3_days", message: "No contact with Priya Sharma for 3+ days", severity: "high" },
  { id: 2, lead_id: 5, type: "missing_documents", message: "3 required documents missing for Sofia Reyes", severity: "medium" },
  { id: 3, lead_id: 8, type: "low_conversion", message: "Low conversion probability (18%) for Omar Hassan", severity: "medium" },
  { id: 4, lead_id: 10, type: "aging_lead", message: "Lead aging score critical (68)", severity: "low" },
];

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>(demoAlerts);

  useEffect(() => {
    api<Alert[]>("/risk/alerts").then(setAlerts).catch(() => {});
  }, []);

  const severityColor: Record<string, string> = {
    high: "var(--hot)",
    medium: "var(--medium)",
    low: "var(--cold)",
  };

  return (
    <div>
      <h1 style={{ fontSize: "1.75rem", marginBottom: 8 }}>Alert Center</h1>
      <p style={{ color: "var(--muted)", marginBottom: 24 }}>AI risk detection — no reply, missing docs, low conversion, aging</p>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {alerts.map((a) => (
          <div key={a.id} className="card" style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
            <AlertTriangle size={22} color={severityColor[a.severity] || "var(--medium)"} />
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
                <span style={{ fontWeight: 600, textTransform: "capitalize" }}>{a.type.replace(/_/g, " ")}</span>
                <span className="badge" style={{ background: "rgba(99,102,241,0.2)", color: severityColor[a.severity] }}>
                  {a.severity}
                </span>
              </div>
              <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>{a.message}</p>
              <span style={{ fontSize: "0.8rem", color: "var(--muted)" }}>Lead #{a.lead_id}</span>
            </div>
            <button className="btn btn-ghost" style={{ fontSize: "0.8rem" }}>Resolve</button>
          </div>
        ))}
      </div>
    </div>
  );
}
