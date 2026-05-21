import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { api } from "../api/client";

export default function Analytics() {
  const [lost, setLost] = useState<{ reason: string; count: number }[]>([
    { reason: "Chose competitor", count: 3 },
    { reason: "Budget constraints", count: 2 },
    { reason: "No response", count: 2 },
    { reason: "Visa concerns", count: 1 },
  ]);
  const [counsellors, setCounsellors] = useState([
    { name: "Priya Nair", leads_assigned: 8, leads_converted: 2, conversion_rate: 25, avg_response_hours: 4.2 },
    { name: "James Mitchell", leads_assigned: 7, leads_converted: 1, conversion_rate: 14.3, avg_response_hours: 5.1 },
  ]);
  const [heatmap, setHeatmap] = useState([
    { doc_type: "Passport Copy", completion_rate: 85 },
    { doc_type: "Academic Transcripts", completion_rate: 72 },
    { doc_type: "Statement of Purpose", completion_rate: 60 },
    { doc_type: "English Proficiency", completion_rate: 45 },
  ]);

  useEffect(() => {
    api<{ reasons: { reason: string; count: number }[] }>("/analytics/lost-reasons")
      .then((r) => setLost(r.reasons))
      .catch(() => {});
    api<typeof counsellors>("/analytics/counsellor-efficiency")
      .then((r) =>
        setCounsellors(
          r.map((c: { name: string; leads_assigned: number; leads_converted: number; conversion_rate: number; avg_response_hours: number }) => ({
            name: c.name,
            leads_assigned: c.leads_assigned,
            leads_converted: c.leads_converted,
            conversion_rate: c.conversion_rate,
            avg_response_hours: c.avg_response_hours,
          }))
        )
      )
      .catch(() => {});
    api<{ doc_type: string; completion_rate: number }[]>("/analytics/document-heatmap")
      .then(setHeatmap)
      .catch(() => {});
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: "1.75rem", marginBottom: 8 }}>Admin Analytics</h1>
      <p style={{ color: "var(--muted)", marginBottom: 28 }}>Lost reasons · Counsellor efficiency · Document heatmap</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>Lost Reason Analytics</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={lost} layout="vertical">
              <XAxis type="number" stroke="#94a3b8" />
              <YAxis dataKey="reason" type="category" width={120} stroke="#94a3b8" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#1a1d27", border: "1px solid #2e3348" }} />
              <Bar dataKey="count" fill="#ef4444" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 16 }}>Document Completion Heatmap</h3>
          {heatmap.map((d) => (
            <div key={d.doc_type} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: 4 }}>
                <span>{d.doc_type}</span>
                <span>{d.completion_rate}%</span>
              </div>
              <div style={{ height: 8, background: "var(--surface2)", borderRadius: 4 }}>
                <div
                  style={{
                    width: `${d.completion_rate}%`,
                    height: "100%",
                    background: d.completion_rate > 70 ? "var(--success)" : d.completion_rate > 50 ? "var(--medium)" : "var(--hot)",
                    borderRadius: 4,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 16 }}>Counsellor Efficiency Dashboard</h3>
        <table>
          <thead>
            <tr>
              <th>Counsellor</th>
              <th>Assigned</th>
              <th>Converted</th>
              <th>Rate</th>
              <th>Avg Response (hrs)</th>
            </tr>
          </thead>
          <tbody>
            {counsellors.map((c) => (
              <tr key={c.name}>
                <td><strong>{c.name}</strong></td>
                <td>{c.leads_assigned}</td>
                <td>{c.leads_converted}</td>
                <td>{c.conversion_rate}%</td>
                <td>{c.avg_response_hours}h</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
