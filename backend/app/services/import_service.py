import csv
import io
from sqlalchemy.orm import Session
from app.models.lead import Lead, LeadSource
from app.services.scoring import assign_tier, compute_conversion_probability, compute_aging_score


SOURCE_MAP = {
    "facebook": LeadSource.FACEBOOK,
    "website": LeadSource.WEBSITE,
    "whatsapp": LeadSource.WHATSAPP_REFERRAL,
    "whatsapp_referral": LeadSource.WHATSAPP_REFERRAL,
    "csv": LeadSource.CSV_IMPORT,
    "google_sheets": LeadSource.GOOGLE_SHEETS,
}


def import_csv(db: Session, content: str) -> dict:
    reader = csv.DictReader(io.StringIO(content))
    created = 0
    errors = []
    for i, row in enumerate(reader, start=2):
        try:
            name = row.get("full_name") or row.get("name") or row.get("Name")
            if not name:
                errors.append(f"Row {i}: missing name")
                continue
            source_raw = (row.get("source") or "csv_import").lower().strip()
            source = SOURCE_MAP.get(source_raw, LeadSource.CSV_IMPORT)
            lead = Lead(
                full_name=name.strip(),
                email=row.get("email") or row.get("Email"),
                phone=row.get("phone") or row.get("Phone"),
                country=row.get("country") or row.get("Country"),
                program_interest=row.get("program_interest") or row.get("program") or row.get("Program"),
                source=source,
                referral_code=row.get("referral_code"),
                notes=row.get("notes"),
            )
            lead.aging_score = compute_aging_score(lead)
            lead.conversion_probability = compute_conversion_probability(lead, 0.3)
            lead.tier = assign_tier(lead.conversion_probability)
            db.add(lead)
            created += 1
        except Exception as e:
            errors.append(f"Row {i}: {e}")
    db.commit()
    return {"imported": created, "errors": errors}
