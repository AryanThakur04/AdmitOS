from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.lead import Lead, LeadStatus
from app.models.alert import Alert, AlertType
from app.models.document import Document, DocumentStatus
from app.services.scoring import compute_conversion_probability, compute_aging_score


def _has_unresolved(db: Session, lead_id: int, alert_type: AlertType) -> bool:
    return (
        db.query(Alert)
        .filter(
            Alert.lead_id == lead_id,
            Alert.type == alert_type,
            Alert.is_resolved == False,
        )
        .first()
        is not None
    )


def scan_lead_risks(db: Session, lead: Lead) -> list[Alert]:
    created = []
    if lead.status == LeadStatus.LOST:
        return created

    ref = lead.last_contact_at or lead.created_at
    if ref is None:
        ref = datetime.utcnow()
    if datetime.utcnow() - ref > timedelta(days=3):
        if not _has_unresolved(db, lead.id, AlertType.NO_REPLY_3_DAYS):
            a = Alert(
                lead_id=lead.id,
                type=AlertType.NO_REPLY_3_DAYS,
                message=f"No contact with {lead.full_name} for 3+ days",
                severity="high",
            )
            db.add(a)
            created.append(a)

    required = (
        db.query(Document)
        .filter(Document.lead_id == lead.id, Document.is_required == True)
        .all()
    )
    missing = [d for d in required if d.status == DocumentStatus.PENDING]
    if missing and lead.status in (LeadStatus.APPLICATION, LeadStatus.QUALIFIED):
        if not _has_unresolved(db, lead.id, AlertType.MISSING_DOCUMENTS):
            a = Alert(
                lead_id=lead.id,
                type=AlertType.MISSING_DOCUMENTS,
                message=f"{len(missing)} required documents missing for {lead.full_name}",
                severity="medium",
            )
            db.add(a)
            created.append(a)

    doc_rate = 1.0 - (len(missing) / max(len(required), 1)) if required else 1.0
    prob = compute_conversion_probability(lead, doc_rate)
    if prob < 0.25:
        if not _has_unresolved(db, lead.id, AlertType.LOW_CONVERSION):
            a = Alert(
                lead_id=lead.id,
                type=AlertType.LOW_CONVERSION,
                message=f"Low conversion probability ({prob:.0%}) for {lead.full_name}",
                severity="medium",
            )
            db.add(a)
            created.append(a)

    if compute_aging_score(lead) > 60:
        if not _has_unresolved(db, lead.id, AlertType.AGING_LEAD):
            a = Alert(
                lead_id=lead.id,
                type=AlertType.AGING_LEAD,
                message=f"Lead aging score critical ({compute_aging_score(lead):.0f})",
                severity="low",
            )
            db.add(a)
            created.append(a)

    return created


def scan_all_leads(db: Session) -> int:
    leads = db.query(Lead).filter(Lead.status != LeadStatus.LOST).all()
    count = 0
    for lead in leads:
        alerts = scan_lead_risks(db, lead)
        count += len(alerts)
    db.commit()
    return count
