import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { api, demoStats } from "../api/client";

const COLORS = ["#6366f1", "#8b5cf6", "#22c55e", "#f59e0b", "#ef4444"];

export default function Dashboard() {
  const [stats, setStats] = useState(demoStats);

  useEffect(() => {
    api<typeof demoStats>("/analytics/dashboard").then(setStats).catch(() => {});
  }, []);

  const sourceData = Object.entries(stats.leads_by_source)
    .filter(([, v]) => v > 0)
    .map(([name, value]) => ({ name: name.replace("_", " "), value }));

  const weekLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const weekData = stats.weekly_new_leads.map((v, i) => ({ day: weekLabels[i] || `D${i}`, leads: v }));

  const kpis = [
    { label: "Total Leads", value: stats.total_leads, color: "var(--primary)" },
    { label: "Hot Leads", value: stats.hot_leads, color: "var(--hot)" },
    { label: "Active Alerts", value: stats.active_alerts, color: "var(--medium)" },
    { label: "Conversion Rate", value: `${stats.conversion_rate}%`, color: "var(--success)" },
    { label: "Avg Aging Score", value: stats.avg_aging_score, color: "var(--cold)" },
  ];

  return (
    <div>
      <h1 style={{ fontSize: "1.75rem", marginBottom: 8 }}>Command Dashboard</h1>
      <p style={{ color: "var(--muted)", marginBottom: 28 }}>Real-time admission operations overview</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 16, marginBottom: 28 }}>
        {kpis.map((k) => (
          <div key={k.label} className="card">
            <div style={{ fontSize: "0.8rem", color: "var(--muted)" }}>{k.label}</div>
            <div style={{ fontSize: "2rem", fontWeight: 700, color: k.color }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>Weekly New Leads</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={weekData}>
              <XAxis dataKey="day" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ background: "#1a1d27", border: "1px solid #2e3348" }} />
              <Bar dataKey="leads" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>Leads by Source</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={sourceData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {sourceData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#1a1d27", border: "1px solid #2e3348" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Pipeline Status</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
          {Object.entries(stats.leads_by_status).map(([status, count]) => (
            <div key={status} style={{ padding: "0.5rem 1rem", background: "var(--surface2)", borderRadius: 8 }}>
              <span style={{ color: "var(--muted)", fontSize: "0.8rem" }}>{status}</span>
              <strong style={{ marginLeft: 8 }}>{count}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
