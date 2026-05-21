from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.lead import LeadSource, LeadStatus, LeadTier


class LeadBase(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    country: str | None = None
    program_interest: str | None = None
    source: LeadSource = LeadSource.WEBSITE
    notes: str | None = None


class LeadCreate(LeadBase):
    counsellor_id: int | None = None
    referral_code: str | None = None
    referred_by_lead_id: int | None = None


class LeadUpdate(BaseModel):
    status: LeadStatus | None = None
    tier: LeadTier | None = None
    counsellor_id: int | None = None
    lost_reason: str | None = None
    notes: str | None = None


class LeadResponse(LeadBase):
    id: int
    status: LeadStatus
    tier: LeadTier
    counsellor_id: int | None
    conversion_probability: float
    aging_score: float
    lost_reason: str | None
    referral_code: str | None
    last_contact_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    items: list[LeadResponse]
    total: int
    page: int
    page_size: int
