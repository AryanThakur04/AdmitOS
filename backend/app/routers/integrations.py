from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import Lead
from app.services.sheets_sync import sync_status, push_leads_to_sheet

router = APIRouter(prefix="/integrations", tags=["Integrations"])


@router.get("/sheets/status")
def sheets_status():
    return sync_status()


@router.post("/sheets/sync")
async def sheets_sync(db: Session = Depends(get_db)):
    leads = db.query(Lead).limit(100).all()
    payload = [
        {
            "id": l.id,
            "name": l.full_name,
            "email": l.email,
            "status": l.status.value,
            "tier": l.tier.value,
        }
        for l in leads
    ]
    return await push_leads_to_sheet(payload)


@router.get("/referral-chain/{lead_id}")
def referral_chain(lead_id: int, db: Session = Depends(get_db)):
    from app.models.referral import ReferralChain

    chains = db.query(ReferralChain).filter(
        (ReferralChain.referrer_lead_id == lead_id)
        | (ReferralChain.referred_lead_id == lead_id)
    ).all()
    nodes = []
    for c in chains:
        ref = db.query(Lead).filter(Lead.id == c.referrer_lead_id).first()
        referred = db.query(Lead).filter(Lead.id == c.referred_lead_id).first()
        nodes.append(
            {
                "referrer": ref.full_name if ref else None,
                "referred": referred.full_name if referred else None,
                "depth": c.depth,
                "code": c.referral_code,
            }
        )
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    return {
        "lead_id": lead_id,
        "referral_code": lead.referral_code if lead else None,
        "chain": nodes,
    }
