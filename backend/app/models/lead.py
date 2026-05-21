import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, Float, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class LeadSource(str, enum.Enum):
    FACEBOOK = "facebook"
    WEBSITE = "website"
    WHATSAPP_REFERRAL = "whatsapp_referral"
    CSV_IMPORT = "csv_import"
    GOOGLE_SHEETS = "google_sheets"


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    APPLICATION = "application"
    ACCEPTED = "accepted"
    LOST = "lost"


class LeadTier(str, enum.Enum):
    HOT = "hot"
    MEDIUM = "medium"
    COLD = "cold"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    program_interest: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[LeadSource] = mapped_column(
        Enum(LeadSource, native_enum=False, length=30), default=LeadSource.WEBSITE
    )
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, native_enum=False, length=20), default=LeadStatus.NEW
    )
    tier: Mapped[LeadTier] = mapped_column(
        Enum(LeadTier, native_enum=False, length=10), default=LeadTier.MEDIUM
    )
    counsellor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    conversion_probability: Mapped[float] = mapped_column(Float, default=0.5)
    aging_score: Mapped[float] = mapped_column(Float, default=0.0)
    lost_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    referral_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    referred_by_lead_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict | None] = mapped_column("meta", JSON, nullable=True)
    last_contact_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    counsellor = relationship("User", back_populates="leads")
    touchpoints = relationship("Touchpoint", back_populates="lead", order_by="Touchpoint.created_at")
    documents = relationship("Document", back_populates="lead")
    alerts = relationship("Alert", back_populates="lead")
