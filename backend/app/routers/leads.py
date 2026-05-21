import logging
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.lead import Lead, LeadStatus, LeadTier, LeadSource
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadListResponse
from app.services.import_service import import_csv
from app.services.scoring import (
    compute_aging_score,
    compute_conversion_probability,
    assign_tier,
)
from app.services.risk_detector import scan_lead_risks
from app.models.document import Document, DocumentStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/leads", tags=["Leads"])


def _doc_completion(db: Session, lead_id: int) -> float:
    docs = db.query(Document).filter(Document.lead_id == lead_id).all()
    if not docs:
        return 0.5
    done = sum(1 for d in docs if d.status != DocumentStatus.PENDING)
    return done / len(docs)


@router.get("", response_model=LeadListResponse)
def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    tier: LeadTier | None = None,
    status: LeadStatus | None = None,
    source: LeadSource | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Lead)
    if tier:
        q = q.filter(Lead.tier == tier)
    if status:
        q = q.filter(Lead.status == status)
    if source:
        q = q.filter(Lead.source == source)
    if search:
        q = q.filter(Lead.full_name.ilike(f"%{search}%"))
    total = q.count()
    items = q.order_by(Lead.updated_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return LeadListResponse(
        items=[LeadResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    return LeadResponse.model_validate(lead)


@router.post("", response_model=LeadResponse)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    try:
        lead = Lead(**data.model_dump())
        lead.aging_score = compute_aging_score(lead)
        dc = 0.3
        lead.conversion_probability = compute_conversion_probability(lead, dc)
        lead.tier = assign_tier(lead.conversion_probability)
        db.add(lead)
        db.commit()
        db.refresh(lead)
        lead.aging_score = compute_aging_score(lead)
        scan_lead_risks(db, lead)
        db.commit()
        db.refresh(lead)
        return LeadResponse.model_validate(lead)
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Failed to create lead")
        raise HTTPException(status_code=500, detail="Database error saving lead") from e
    except Exception as e:
        db.rollback()
        logger.exception("Failed to create lead")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, data: LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(lead, k, v)
    dc = _doc_completion(db, lead.id)
    lead.aging_score = compute_aging_score(lead)
    lead.conversion_probability = compute_conversion_probability(lead, dc)
    lead.tier = assign_tier(lead.conversion_probability)
    db.commit()
    db.refresh(lead)
    scan_lead_risks(db, lead)
    db.commit()
    return LeadResponse.model_validate(lead)


@router.post("/import")
async def import_leads(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = (await file.read()).decode("utf-8")
    return import_csv(db, content)
