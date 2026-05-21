# Integrations

## Google Sheets

Set in `.env`:
```
GOOGLE_SHEETS_CREDENTIALS_JSON=/path/to/service-account.json
GOOGLE_SHEET_ID=your-sheet-id
```

```bash
GET /api/v1/integrations/sheets/status
POST /api/v1/integrations/sheets/sync
```

## CSV Import

Upload to `POST /api/v1/leads/import` with columns:
`full_name, email, phone, country, program_interest, source, notes`

Sample file: `data/sample_leads.csv`

## WhatsApp

Configure `WHATSAPP_API_TOKEN` for production webhooks. Demo uses the **WhatsApp Follow-up Simulator** in AI Tools.

## AI Providers

Set `AI_PROVIDER=gemini` or use OpenAI. Demo mode works without API keys.
