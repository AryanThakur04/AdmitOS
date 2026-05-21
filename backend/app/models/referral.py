from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ReferralChain(Base):
    __tablename__ = "referral_chains"

    id: Mapped[int] = mapped_column(primary_key=True)
    referrer_lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    referred_lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    depth: Mapped[int] = mapped_column(Integer, default=1)
    referral_code: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
