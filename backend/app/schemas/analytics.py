from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_leads: int
    hot_leads: int
    medium_leads: int
    cold_leads: int
    active_alerts: int
    conversion_rate: float
    avg_aging_score: float
    leads_by_source: dict[str, int]
    leads_by_status: dict[str, int]
    weekly_new_leads: list[int]


class LostReasonStats(BaseModel):
    reasons: list[dict]
    total_lost: int


class CounsellorEfficiency(BaseModel):
    counsellor_id: int
    name: str
    email: str
    leads_assigned: int
    leads_converted: int
    conversion_rate: float
    avg_response_hours: float
    active_alerts: int


class DocumentHeatmapItem(BaseModel):
    doc_type: str
    completion_rate: float
    pending: int
    verified: int


class JourneyEvent(BaseModel):
    id: int
    type: str
    title: str
    content: str | None
    created_at: str
    created_by: str | None


class ConversionPrediction(BaseModel):
    lead_id: int
    probability: float
    tier: str
    factors: list[str]
    recommendation: str
