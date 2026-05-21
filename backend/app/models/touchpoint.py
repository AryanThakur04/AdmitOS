import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class TouchpointType(str, enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    CALL = "call"
    MEETING = "meeting"
    NOTE = "note"
    STATUS_CHANGE = "status_change"
    AI_SUMMARY = "ai_summary"


class Touchpoint(Base):
    __tablename__ = "touchpoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    type: Mapped[TouchpointType] = mapped_column(Enum(TouchpointType))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="touchpoints")
