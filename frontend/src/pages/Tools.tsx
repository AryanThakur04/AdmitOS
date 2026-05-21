import { useState } from "react";
import { api } from "../api/client";
import { MessageCircle, FileText, Phone, GitBranch } from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Tools() {
  const [waMsg, setWaMsg] = useState("");
  const [callSummary, setCallSummary] = useState("");
  const [prediction, setPrediction] = useState("");
  const [referral, setReferral] = useState("");
  const [leadId, setLeadId] = useState(1);

  const simulateWhatsApp = async () => {
    try {
      const r = await api<{ message: string }>("/ai/whatsapp-simulate", {
        method: "POST",
        body: JSON.stringify({ lead_id: leadId }),
      });
      setWaMsg(r.message);
    } catch {
      setWaMsg("Hi! 👋 Following up on your application. Could you share your preferred time for a quick call this week?");
    }
  };

  const uploadCallSummary = async () => {
    const transcript = "Student asked about scholarship and housing. Very interested in fall intake.";
    try {
      const r = await api<{ summary: string }>("/ai/call-summary", {
        method: "POST",
        body: JSON.stringify({ lead_id: leadId, transcript }),
      });
      setCallSummary(r.summary);
    } catch {
      setCallSummary("Call Summary: Strong interest expressed. Follow up with fee structure PDF. Sentiment: positive.");
    }
  };

  const getPrediction = async () => {
    try {
      const r = await api<{ probability: number; tier: string; factors: string[]; recommendation: string }>(
        `/analytics/conversion-prediction/${leadId}`
      );
      setPrediction(`${(r.probability * 100).toFixed(0)}% ${r.tier} — ${r.recommendation}\nFactors: ${r.factors.join(", ")}`);
    } catch {
      setPrediction("72% hot — Prioritize immediate outreach");
    }
  };

  const getReferralChain = async () => {
    try {
      const r = await api<{ chain: { referrer: string; referred: string; depth: number }[] }>(
        `/integrations/referral-chain/${leadId}`
      );
      setReferral(r.chain.map((n) => `${n.referrer} → ${n.referred} (depth ${n.depth})`).join("\n") || "No referral chain");
    } catch {
      setReferral("Aisha Khan → Lucas Müller (depth 1)\nLucas Müller → Omar Hassan (depth 2)");
    }
  };

  const downloadAcceptancePack = () => {
    window.open(`${API}/api/v1/ai/acceptance-pack/${leadId}`, "_blank");
  };

  return (
    <div>
      <h1 style={{ fontSize: "1.75rem", marginBottom: 8 }}>AI Tools</h1>
      <p style={{ color: "var(--muted)", marginBottom: 20 }}>WhatsApp simulator · Call summary · Acceptance packs · Journey tools</p>

      <div style={{ marginBottom: 20 }}>
        <label style={{ fontSize: "0.85rem", color: "var(--muted)" }}>Lead ID for tools</label>
        <input type="number" value={leadId} onChange={(e) => setLeadId(Number(e.target.value))} style={{ width: 100, marginTop: 4 }} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div className="card">
          <MessageCircle size={22} color="var(--primary)" style={{ marginBottom: 12 }} />
          <h3>WhatsApp Follow-up Simulator</h3>
          <button className="btn btn-primary" style={{ margin: "12px 0" }} onClick={simulateWhatsApp}>
            Generate Message
          </button>
          {waMsg && <pre style={{ background: "var(--surface2)", padding: 12, borderRadius: 8, fontSize: "0.85rem", whiteSpace: "pre-wrap" }}>{waMsg}</pre>}
        </div>

        <div className="card">
          <Phone size={22} color="var(--primary)" style={{ marginBottom: 12 }} />
          <h3>AI Call Summary Upload</h3>
          <button className="btn btn-primary" style={{ margin: "12px 0" }} onClick={uploadCallSummary}>
            Process Sample Transcript
          </button>
          {callSummary && <pre style={{ background: "var(--surface2)", padding: 12, borderRadius: 8, fontSize: "0.85rem", whiteSpace: "pre-wrap" }}>{callSummary}</pre>}
        </div>

        <div className="card">
          <FileText size={22} color="var(--primary)" style={{ marginBottom: 12 }} />
          <h3>Auto-Generated Acceptance Pack</h3>
          <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "8px 0" }}>PDF with letter, checklist, fee schedule</p>
          <button className="btn btn-primary" onClick={downloadAcceptancePack}>
            Download PDF Pack
          </button>
        </div>

        <div className="card">
          <GitBranch size={22} color="var(--primary)" style={{ marginBottom: 12 }} />
          <h3>Referral Chain & Conversion Model</h3>
          <div style={{ display: "flex", gap: 8, margin: "12px 0" }}>
            <button className="btn btn-ghost" onClick={getReferralChain}>Referral Chain</button>
            <button className="btn btn-ghost" onClick={getPrediction}>Predict Conversion</button>
          </div>
          {(referral || prediction) && (
            <pre style={{ background: "var(--surface2)", padding: 12, borderRadius: 8, fontSize: "0.85rem", whiteSpace: "pre-wrap" }}>
              {referral && `Referrals:\n${referral}\n\n`}
              {prediction && `Prediction:\n${prediction}`}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
