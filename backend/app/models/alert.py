import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class AlertType(str, enum.Enum):
    NO_REPLY_3_DAYS = "no_reply_3_days"
    MISSING_DOCUMENTS = "missing_documents"
    LOW_CONVERSION = "low_conversion"
    AGING_LEAD = "aging_lead"
    SLA_BREACH = "sla_breach"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    type: Mapped[AlertType] = mapped_column(Enum(AlertType, native_enum=False, length=30))
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="alerts")
