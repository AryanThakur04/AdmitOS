# Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│   React     │────▶│   FastAPI    │────▶│  PostgreSQL    │
│  Dashboard  │     │     API      │     │                │
└─────────────┘     └──────┬───────┘     └────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌──────────┐    ┌─────────────┐   ┌──────────────┐
   │ Gemini/  │    │   Google    │   │  WhatsApp    │
   │ OpenAI   │    │   Sheets    │   │  (webhook)   │
   └──────────┘    └─────────────┘   └──────────────┘
```

## Backend Layers

| Layer | Path | Role |
|-------|------|------|
| Routers | `app/routers/` | HTTP endpoints |
| Services | `app/services/` | Business logic, AI, scoring |
| Models | `app/models/` | SQLAlchemy ORM |
| Schemas | `app/schemas/` | Pydantic validation |

## Key Services

- **scoring.py** — Tier, aging, conversion probability
- **risk_detector.py** — Alert generation rules
- **ai_service.py** — LLM integration with demo fallback
- **import_service.py** — CSV lead import
- **acceptance_pack.py** — PDF generation (ReportLab)

## Data Model

- `users` — Admin & counsellors
- `leads` — Core CRM entity
- `touchpoints` — Journey events
- `documents` — Per-lead doc tracking
- `alerts` — Risk notifications
- `referral_chains` — Referral graph edges
