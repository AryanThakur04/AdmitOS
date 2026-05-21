# AdmitOS — Autonomous Education Operations Engine

<p align="center">
  <img src="assets/logo.svg" alt="AdmitOS Logo" width="120"/>
</p>

**AdmitOS** is an AI-powered admission operating system that unifies lead intake, counsellor workflows, risk detection, and predictive analytics for education institutions.

[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7)](docs/DEPLOYMENT.md)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL-blue)](docs/wiki/Architecture.md)

---

## Features

| Module | Capabilities |
|--------|-------------|
| **Lead Intake** | CSV import, Google Sheets sync, Facebook / Website / WhatsApp sources |
| **AI Scoring** | Hot / Medium / Cold leads, lead aging score, conversion prediction |
| **Risk Detector** | No reply 3+ days, missing documents, low conversion probability |
| **Counsellor Analytics** | Efficiency dashboard, lost-reason analytics |
| **Document Engine** | Completion heatmaps, auto-generated acceptance packs |
| **WhatsApp** | Follow-up simulator, referral chain tracking |
| **Journey Replay** | Full student timeline with touchpoints |
| **Alert Center** | Real-time risk and SLA notifications |
| **Admin Command** | Daily reporting pipeline, analytics API |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker)

### 1. Clone & configure

```bash
git clone https://github.com/your-org/admitos.git
cd admitos
cp .env.example .env
```

### 2. Run with Docker (recommended)

```bash
docker compose up --build
```

- **API**: http://localhost:8000/docs
- **Dashboard**: http://localhost:5173
- **Landing**: http://localhost:5173/

### 3. Seed demo data

```bash
docker compose exec api python -m app.seed
```

### Demo logins

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@admitos.demo | demo1234 |
| Counsellor | priya@admitos.demo | demo1234 |
| Counsellor | james@admitos.demo | demo1234 |

---

## Project Structure

```
admitos/
├── backend/          # FastAPI + PostgreSQL
├── frontend/         # React + Vite dashboard
├── data/             # Sample CSV leads
├── docs/             # Deployment, wiki, screenshots
├── assets/           # Logo & brand assets
└── docker-compose.yml
```

---

## API Overview

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/leads` | List leads with filters |
| `POST /api/v1/leads/import` | CSV import |
| `GET /api/v1/analytics/dashboard` | Admin KPIs |
| `GET /api/v1/analytics/lost-reasons` | Lost reason breakdown |
| `GET /api/v1/analytics/counsellor-efficiency` | Counsellor metrics |
| `GET /api/v1/risk/alerts` | Active risk alerts |
| `POST /api/v1/ai/score-lead/{id}` | Re-score lead with AI |
| `POST /api/v1/ai/whatsapp-simulate` | WhatsApp follow-up preview |
| `GET /api/v1/journey/{lead_id}` | Student journey replay |
| `POST /api/v1/documents/acceptance-pack/{id}` | Generate acceptance pack |

Full OpenAPI docs at `/docs` when the API is running.

---

## Environment Variables

See [.env.example](.env.example). Key variables:

- `DATABASE_URL` — PostgreSQL connection string
- `GEMINI_API_KEY` or `OPENAI_API_KEY` — AI features (optional for demo)
- `GOOGLE_SHEETS_CREDENTIALS_JSON` — Sheets sync (optional)

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) and [docs/wiki/Home.md](docs/wiki/Home.md).

---

## License

MIT — built as a portfolio / startup demo project.
