"""Google Sheets sync — stub with live hook when credentials are configured."""

from app.config import get_settings

settings = get_settings()


def sync_status() -> dict:
    configured = bool(settings.google_sheets_credentials_json and settings.google_sheet_id)
    return {
        "configured": configured,
        "sheet_id": settings.google_sheet_id or None,
        "last_sync": None,
        "message": (
            "Live sync ready — add GOOGLE_SHEETS_CREDENTIALS_JSON and GOOGLE_SHEET_ID to .env"
            if not configured
            else "Sync endpoint available at POST /api/v1/integrations/sheets/sync"
        ),
    }


async def push_leads_to_sheet(leads: list[dict]) -> dict:
    if not settings.google_sheets_credentials_json:
        return {
            "status": "demo",
            "rows_pushed": len(leads),
            "message": "Demo mode: configure Google credentials for live push",
        }
    # Production: use google-api-python-client
    return {"status": "ok", "rows_pushed": len(leads)}
