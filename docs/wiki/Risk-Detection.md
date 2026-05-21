# Risk Detection

Automated rules engine scans leads and creates alerts.

## Alert Types

| Type | Trigger |
|------|---------|
| `no_reply_3_days` | No contact for 3+ days |
| `missing_documents` | Required docs pending at application stage |
| `low_conversion` | Probability < 25% |
| `aging_lead` | Aging score > 60 |

## Running Scans

```bash
POST /api/v1/risk/scan
GET /api/v1/risk/alerts
```

Scans also run automatically on lead create/update.
