from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.alert import Alert
from app.services.risk_detector import scan_all_leads

router = APIRouter(prefix="/risk", tags=["Risk & Alerts"])


class AlertResponse(BaseModel):
    id: int
    lead_id: int
    type: str
    message: str
    severity: str
    is_resolved: bool
    created_at: str

    class Config:
        from_attributes = True


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(resolved: bool = False, db: Session = Depends(get_db)):
    q = db.query(Alert)
    if not resolved:
        q = q.filter(Alert.is_resolved == False)
    alerts = q.order_by(Alert.created_at.desc()).limit(50).all()
    return [
        AlertResponse(
            id=a.id,
            lead_id=a.lead_id,
            type=a.type.value,
            message=a.message,
            severity=a.severity,
            is_resolved=a.is_resolved,
            created_at=a.created_at.isoformat(),
        )
        for a in alerts
    ]


@router.post("/scan")
def run_risk_scan(db: Session = Depends(get_db)):
    count = scan_all_leads(db)
    return {"new_alerts": count}


@router.patch("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_resolved = True
        db.commit()
    return {"resolved": True}
