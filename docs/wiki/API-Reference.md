# API Reference

Base URL: `http://localhost:8000/api/v1`

## Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/login` | Login with email/password |
| GET | `/auth/me` | Current user |

## Leads
| Method | Path | Description |
|--------|------|-------------|
| GET | `/leads` | List with filters |
| GET | `/leads/{id}` | Single lead |
| POST | `/leads` | Create lead |
| PATCH | `/leads/{id}` | Update lead |
| POST | `/leads/import` | CSV file upload |

## Analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | `/analytics/dashboard` | KPI dashboard |
| GET | `/analytics/lost-reasons` | Lost reason breakdown |
| GET | `/analytics/counsellor-efficiency` | Counsellor metrics |
| GET | `/analytics/document-heatmap` | Doc completion rates |
| GET | `/analytics/journey/{id}` | Student journey replay |
| GET | `/analytics/conversion-prediction/{id}` | ML-style prediction |

## AI
| Method | Path | Description |
|--------|------|-------------|
| POST | `/ai/score-lead/{id}` | Re-score lead |
| POST | `/ai/whatsapp-simulate` | Generate WA message |
| POST | `/ai/call-summary` | Transcript → summary |
| POST | `/ai/acceptance-pack/{id}` | Download PDF pack |

## Risk
| Method | Path | Description |
|--------|------|-------------|
| GET | `/risk/alerts` | Active alerts |
| POST | `/risk/scan` | Run full risk scan |
| PATCH | `/risk/alerts/{id}/resolve` | Resolve alert |

## Integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | `/integrations/sheets/status` | Sheets config status |
| POST | `/integrations/sheets/sync` | Push leads to sheet |
| GET | `/integrations/referral-chain/{id}` | Referral graph |
