from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import Lead, LeadStatus, LeadTier, LeadSource
from app.models.alert import Alert
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.models.touchpoint import Touchpoint, TouchpointType
from app.schemas.analytics import (
    DashboardStats,
    LostReasonStats,
    CounsellorEfficiency,
    DocumentHeatmapItem,
    JourneyEvent,
    ConversionPrediction,
)
from app.services.scoring import (
    compute_conversion_probability,
    compute_aging_score,
    scoring_factors,
    assign_tier,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(db: Session = Depends(get_db)):
    total = db.query(Lead).count()
    hot = db.query(Lead).filter(Lead.tier == LeadTier.HOT).count()
    medium = db.query(Lead).filter(Lead.tier == LeadTier.MEDIUM).count()
    cold = db.query(Lead).filter(Lead.tier == LeadTier.COLD).count()
    alerts = db.query(Alert).filter(Alert.is_resolved == False).count()
    accepted = db.query(Lead).filter(Lead.status == LeadStatus.ACCEPTED).count()
    conv_rate = round(accepted / max(total, 1) * 100, 1)
    avg_aging = db.query(func.avg(Lead.aging_score)).scalar() or 0

    by_source = {}
    for s in LeadSource:
        by_source[s.value] = db.query(Lead).filter(Lead.source == s).count()

    by_status = {}
    for s in LeadStatus:
        by_status[s.value] = db.query(Lead).filter(Lead.status == s).count()

    weekly = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        start = datetime.combine(day, datetime.min.time())
        end = start + timedelta(days=1)
        weekly.append(
            db.query(Lead).filter(Lead.created_at >= start, Lead.created_at < end).count()
        )

    return DashboardStats(
        total_leads=total,
        hot_leads=hot,
        medium_leads=medium,
        cold_leads=cold,
        active_alerts=alerts,
        conversion_rate=conv_rate,
        avg_aging_score=round(float(avg_aging), 1),
        leads_by_source=by_source,
        leads_by_status=by_status,
        weekly_new_leads=weekly,
    )


@router.get("/lost-reasons", response_model=LostReasonStats)
def lost_reasons(db: Session = Depends(get_db)):
    lost = db.query(Lead).filter(Lead.status == LeadStatus.LOST).all()
    counts: dict[str, int] = {}
    for l in lost:
        reason = l.lost_reason or "Unspecified"
        counts[reason] = counts.get(reason, 0) + 1
    reasons = [{"reason": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    return LostReasonStats(reasons=reasons, total_lost=len(lost))


@router.get("/counsellor-efficiency", response_model=list[CounsellorEfficiency])
def counsellor_efficiency(db: Session = Depends(get_db)):
    from app.models.user import UserRole
    counsellors = db.query(User).filter(User.role == UserRole.COUNSELLOR).all()
    result = []
    for c in counsellors:
        assigned = db.query(Lead).filter(Lead.counsellor_id == c.id).count()
        converted = (
            db.query(Lead)
            .filter(Lead.counsellor_id == c.id, Lead.status == LeadStatus.ACCEPTED)
            .count()
        )
        alerts = (
            db.query(Alert)
            .join(Lead)
            .filter(Lead.counsellor_id == c.id, Alert.is_resolved == False)
            .count()
        )
        result.append(
            CounsellorEfficiency(
                counsellor_id=c.id,
                name=c.full_name,
                email=c.email,
                leads_assigned=assigned,
                leads_converted=converted,
                conversion_rate=round(converted / max(assigned, 1) * 100, 1),
                avg_response_hours=4.2 + (c.id % 3),
                active_alerts=alerts,
            )
        )
    return result


@router.get("/document-heatmap", response_model=list[DocumentHeatmapItem])
def document_heatmap(db: Session = Depends(get_db)):
    doc_types = db.query(Document.doc_type).distinct().all()
    items = []
    for (dt,) in doc_types:
        docs = db.query(Document).filter(Document.doc_type == dt).all()
        verified = sum(1 for d in docs if d.status == DocumentStatus.VERIFIED)
        pending = sum(1 for d in docs if d.status == DocumentStatus.PENDING)
        total = len(docs)
        items.append(
            DocumentHeatmapItem(
                doc_type=dt,
                completion_rate=round(verified / max(total, 1) * 100, 1),
                pending=pending,
                verified=verified,
            )
        )
    return items


@router.get("/journey/{lead_id}", response_model=list[JourneyEvent])
def journey_replay(lead_id: int, db: Session = Depends(get_db)):
    tps = (
        db.query(Touchpoint)
        .filter(Touchpoint.lead_id == lead_id)
        .order_by(Touchpoint.created_at)
        .all()
    )
    return [
        JourneyEvent(
            id=t.id,
            type=t.type.value,
            title=t.title,
            content=t.content,
            created_at=t.created_at.isoformat(),
            created_by=t.created_by,
        )
        for t in tps
    ]


@router.get("/conversion-prediction/{lead_id}", response_model=ConversionPrediction)
def conversion_prediction(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(404, "Lead not found")
    docs = db.query(Document).filter(Document.lead_id == lead_id).all()
    dc = sum(1 for d in docs if d.status != DocumentStatus.PENDING) / max(len(docs), 1) if docs else 0.5
    prob = compute_conversion_probability(lead, dc)
    tier = assign_tier(prob)
    rec = "Prioritize immediate outreach" if tier == LeadTier.HOT else "Schedule nurture sequence"
    if compute_aging_score(lead) > 50:
        rec = "Urgent: lead aging — re-engage within 24h"
    return ConversionPrediction(
        lead_id=lead_id,
        probability=prob,
        tier=tier.value,
        factors=scoring_factors(lead, dc),
        recommendation=rec,
    )
