import { Link } from "react-router-dom";
import {
  Zap,
  Shield,
  MessageCircle,
  BarChart3,
  FileCheck,
  GitBranch,
} from "lucide-react";

const features = [
  { icon: Zap, title: "AI Lead Scoring", desc: "Hot / Medium / Cold tiers with conversion prediction" },
  { icon: Shield, title: "Risk Detector", desc: "No-reply, missing docs, aging leads — auto alerts" },
  { icon: MessageCircle, title: "WhatsApp Simulator", desc: "AI-generated follow-up messages before you send" },
  { icon: BarChart3, title: "Counsellor Analytics", desc: "Efficiency dashboards & lost-reason insights" },
  { icon: FileCheck, title: "Acceptance Packs", desc: "Auto-generated PDF enrollment packages" },
  { icon: GitBranch, title: "Referral Chains", desc: "Track multi-level student referrals" },
];

const modules = [
  "Lead Intake System",
  "AI Risk Detector",
  "Counsellor Performance",
  "Document Workflow",
  "WhatsApp Automation",
  "Daily Reporting",
  "Predictive Conversion",
  "Alert Center",
  "Google Sheets Sync",
];

export default function Landing() {
  return (
    <div>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "1.25rem 3rem",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <img src="/logo.svg" alt="AdmitOS" width={40} height={40} />
          <span style={{ fontWeight: 700, fontSize: "1.25rem" }}>AdmitOS</span>
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          <a href="https://github.com" className="btn btn-ghost" style={{ textDecoration: "none" }}>
            GitHub
          </a>
          <Link to="/dashboard" className="btn btn-primary" style={{ textDecoration: "none" }}>
            Open Demo Dashboard
          </Link>
        </div>
      </header>

      <section style={{ textAlign: "center", padding: "5rem 2rem 3rem", maxWidth: 900, margin: "0 auto" }}>
        <div
          style={{
            display: "inline-block",
            padding: "0.35rem 1rem",
            borderRadius: 999,
            background: "rgba(99,102,241,0.15)",
            color: "var(--primary)",
            fontSize: "0.85rem",
            fontWeight: 600,
            marginBottom: 24,
          }}
        >
          Autonomous Education Operations Engine
        </div>
        <h1 style={{ fontSize: "3rem", fontWeight: 800, lineHeight: 1.15, marginBottom: 20 }}>
          The AI Admission
          <br />
          <span style={{ background: "linear-gradient(135deg, var(--primary), var(--primary2))", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            Operating System
          </span>
        </h1>
        <p style={{ color: "var(--muted)", fontSize: "1.15rem", maxWidth: 600, margin: "0 auto 32px" }}>
          Unify Facebook, website, and WhatsApp leads. Score, detect risk, automate follow-ups,
          and generate acceptance packs — one platform for modern admissions teams.
        </p>
        <div style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
          <Link to="/dashboard" className="btn btn-primary" style={{ padding: "0.85rem 2rem", fontSize: "1rem", textDecoration: "none" }}>
            Try Live Demo
          </Link>
          <a href="/docs" className="btn btn-ghost" style={{ padding: "0.85rem 2rem", textDecoration: "none" }}>
            Read Docs
          </a>
        </div>
        <p style={{ marginTop: 20, fontSize: "0.85rem", color: "var(--muted)" }}>
          Demo: admin@admitos.demo / demo1234
        </p>
      </section>

      <section style={{ padding: "3rem 2rem", maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 20 }}>
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card">
              <Icon size={28} color="var(--primary)" style={{ marginBottom: 12 }} />
              <h3 style={{ marginBottom: 8 }}>{title}</h3>
              <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>{desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ padding: "3rem 2rem", background: "var(--surface)", borderTop: "1px solid var(--border)" }}>
        <h2 style={{ textAlign: "center", marginBottom: 24 }}>9 Integrated Modules</h2>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, justifyContent: "center", maxWidth: 800, margin: "0 auto" }}>
          {modules.map((m) => (
            <span key={m} style={{ padding: "0.5rem 1rem", background: "var(--surface2)", borderRadius: 8, fontSize: "0.85rem" }}>
              {m}
            </span>
          ))}
        </div>
      </section>

      <section style={{ padding: "4rem 2rem", textAlign: "center" }}>
        <h2 style={{ marginBottom: 12 }}>Built for CRM · WhatsApp · AI Audits</h2>
        <p style={{ color: "var(--muted)", maxWidth: 500, margin: "0 auto 24px" }}>
          FastAPI · PostgreSQL · React · Gemini/OpenAI · Google Sheets · AWS/Render ready
        </p>
        <Link to="/dashboard" className="btn btn-primary" style={{ textDecoration: "none" }}>
          Launch Dashboard →
        </Link>
      </section>

      <footer style={{ textAlign: "center", padding: "2rem", color: "var(--muted)", fontSize: "0.85rem", borderTop: "1px solid var(--border)" }}>
        © 2026 AdmitOS · MIT License · Portfolio Demo Project
      </footer>
    </div>
  );
}
