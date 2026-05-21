import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Bell,
  BarChart3,
  Wrench,
  LogOut,
} from "lucide-react";

const nav = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/leads", icon: Users, label: "Leads" },
  { to: "/alerts", icon: Bell, label: "Alert Center" },
  { to: "/analytics", icon: BarChart3, label: "Analytics" },
  { to: "/tools", icon: Wrench, label: "AI Tools" },
];

export default function DashboardLayout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: 240,
          background: "var(--surface)",
          borderRight: "1px solid var(--border)",
          padding: "1.5rem 1rem",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 32 }}>
          <img src="/logo.svg" alt="" width={36} height={36} />
          <div>
            <div style={{ fontWeight: 700, fontSize: "1.1rem" }}>AdmitOS</div>
            <div style={{ fontSize: "0.7rem", color: "var(--muted)" }}>Operations Engine</div>
          </div>
        </div>
        <nav style={{ flex: 1, display: "flex", flexDirection: "column", gap: 4 }}>
          {nav.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              style={({ isActive }) => ({
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "0.65rem 0.85rem",
                borderRadius: 8,
                color: isActive ? "white" : "var(--muted)",
                background: isActive ? "linear-gradient(135deg, var(--primary), var(--primary2))" : "transparent",
                fontWeight: isActive ? 600 : 400,
              })}
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <a href="/" style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--muted)", fontSize: "0.85rem", marginTop: 16 }}>
          <LogOut size={16} /> Exit demo
        </a>
      </aside>
      <main style={{ flex: 1, padding: "2rem", overflow: "auto" }}>
        <Outlet />
      </main>
    </div>
  );
}
