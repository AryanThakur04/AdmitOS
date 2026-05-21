from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.lead import Lead
from app.models.touchpoint import Touchpoint, TouchpointType
from app.services.ai_service import (
    whatsapp_followup_simulate,
    generate_acceptance_letter,
    summarize_call_transcript,
)
from app.services.acceptance_pack import generate_acceptance_pack_pdf
from app.services.scoring import compute_conversion_probability, assign_tier
from app.models.document import Document, DocumentStatus

router = APIRouter(prefix="/ai", tags=["AI"])


class WhatsAppSimRequest(BaseModel):
    lead_id: int


class CallSummaryRequest(BaseModel):
    lead_id: int
    transcript: str


@router.post("/score-lead/{lead_id}")
async def score_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    docs = db.query(Document).filter(Document.lead_id == lead_id).all()
    dc = sum(1 for d in docs if d.status != DocumentStatus.PENDING) / max(len(docs), 1) if docs else 0.5
    lead.conversion_probability = compute_conversion_probability(lead, dc)
    lead.tier = assign_tier(lead.conversion_probability)
    db.commit()
    return {"lead_id": lead_id, "tier": lead.tier.value, "probability": lead.conversion_probability}


@router.post("/whatsapp-simulate")
async def whatsapp_simulate(req: WhatsAppSimRequest, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == req.lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    from datetime import datetime
    days = (datetime.utcnow() - (lead.last_contact_at or lead.created_at)).days
    return await whatsapp_followup_simulate(lead.full_name, lead.program_interest or "our program", days)


@router.post("/call-summary")
async def call_summary(req: CallSummaryRequest, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == req.lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    summary = await summarize_call_transcript(req.transcript, lead.full_name)
    tp = Touchpoint(
        lead_id=lead.id,
        type=TouchpointType.AI_SUMMARY,
        title="AI Call Summary",
        content=summary,
        created_by="AdmitOS AI",
    )
    db.add(tp)
    db.commit()
    return {"summary": summary, "touchpoint_id": tp.id}


@router.post("/acceptance-pack/{lead_id}")
async def acceptance_pack(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    letter = await generate_acceptance_letter(
        lead.full_name, lead.program_interest or "Selected Program"
    )
    pdf = generate_acceptance_pack_pdf(
        lead.full_name, lead.program_interest or "Selected Program", letter
    )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="acceptance_{lead_id}.pdf"'},
    )
