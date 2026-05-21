import { useEffect, useState } from "react";
import { api } from "../api/client";

interface Lead {
  id: number;
  full_name: string;
  email: string | null;
  country: string | null;
  program_interest: string | null;
  source: string;
  status: string;
  tier: string;
  conversion_probability: number;
  aging_score: number;
}

const demoLeads: Lead[] = [
  { id: 1, full_name: "Aisha Khan", email: "aisha.k@email.com", country: "UAE", program_interest: "MBA", source: "facebook", status: "qualified", tier: "hot", conversion_probability: 0.78, aging_score: 12 },
  { id: 2, full_name: "James Okafor", email: "j.okafor@email.com", country: "Nigeria", program_interest: "Computer Science", source: "website", status: "application", tier: "hot", conversion_probability: 0.72, aging_score: 8 },
  { id: 3, full_name: "Priya Sharma", email: "priya.s@email.com", country: "India", program_interest: "Data Science", source: "whatsapp_referral", status: "contacted", tier: "medium", conversion_probability: 0.55, aging_score: 24 },
];

export default function Leads() {
  const [leads, setLeads] = useState<Lead[]>(demoLeads);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    api<{ items: Lead[] }>("/leads?page_size=50")
      .then((r) => setLeads(r.items))
      .catch(() => {});
  }, []);

  const filtered = leads.filter((l) =>
    !filter || l.full_name.toLowerCase().includes(filter.toLowerCase()) || l.tier === filter
  );

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: "1.75rem" }}>Lead Pipeline</h1>
          <p style={{ color: "var(--muted)" }}>Import from CSV · Facebook · Website · WhatsApp</p>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <input placeholder="Search leads..." value={filter} onChange={(e) => setFilter(e.target.value)} style={{ width: 200 }} />
          <select value={filter} onChange={(e) => setFilter(e.target.value)} style={{ width: 120 }}>
            <option value="">All tiers</option>
            <option value="hot">Hot</option>
            <option value="medium">Medium</option>
            <option value="cold">Cold</option>
          </select>
        </div>
      </div>

      <div className="card" style={{ overflow: "auto" }}>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Program</th>
              <th>Source</th>
              <th>Status</th>
              <th>Tier</th>
              <th>Conversion</th>
              <th>Aging</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((l) => (
              <tr key={l.id}>
                <td>
                  <strong>{l.full_name}</strong>
                  <div style={{ fontSize: "0.8rem", color: "var(--muted)" }}>{l.country}</div>
                </td>
                <td>{l.program_interest}</td>
                <td>{l.source?.replace("_", " ")}</td>
                <td>{l.status}</td>
                <td><span className={`badge ${l.tier}`}>{l.tier}</span></td>
                <td>{(l.conversion_probability * 100).toFixed(0)}%</td>
                <td>
                  <div style={{ width: 60, height: 6, background: "var(--surface2)", borderRadius: 4 }}>
                    <div style={{ width: `${Math.min(l.aging_score, 100)}%`, height: "100%", background: l.aging_score > 50 ? "var(--hot)" : "var(--primary)", borderRadius: 4 }} />
                  </div>
                  <span style={{ fontSize: "0.75rem", color: "var(--muted)" }}>{l.aging_score}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
