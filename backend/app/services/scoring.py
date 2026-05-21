from datetime import datetime, timedelta
from app.models.lead import Lead, LeadTier, LeadStatus


def compute_aging_score(lead: Lead) -> float:
    """0-100: higher = lead has been inactive longer."""
    ref = lead.last_contact_at or lead.created_at
    if ref is None:
        return 0.0
    days = max(0, (datetime.utcnow() - ref).days)
    return min(100.0, days * 8.0)


def compute_conversion_probability(lead: Lead, doc_completion: float) -> float:
    score = 0.35
    tier_map = {LeadTier.HOT: 0.35, LeadTier.MEDIUM: 0.15, LeadTier.COLD: -0.15}
    score += tier_map.get(lead.tier, 0)
    status_map = {
        LeadStatus.NEW: 0.05,
        LeadStatus.CONTACTED: 0.1,
        LeadStatus.QUALIFIED: 0.2,
        LeadStatus.APPLICATION: 0.3,
        LeadStatus.ACCEPTED: 0.5,
        LeadStatus.LOST: -0.5,
    }
    score += status_map.get(lead.status, 0)
    score += doc_completion * 0.25
    aging = compute_aging_score(lead)
    if aging > 50:
        score -= 0.15
    if lead.source.value == "whatsapp_referral":
        score += 0.1
    return max(0.05, min(0.95, round(score, 2)))


def assign_tier(probability: float) -> LeadTier:
    if probability >= 0.65:
        return LeadTier.HOT
    if probability >= 0.4:
        return LeadTier.MEDIUM
    return LeadTier.COLD


def scoring_factors(lead: Lead, doc_completion: float) -> list[str]:
    factors = []
    if lead.tier == LeadTier.HOT:
        factors.append("High engagement tier")
    if lead.status in (LeadStatus.APPLICATION, LeadStatus.QUALIFIED):
        factors.append("Advanced pipeline stage")
    if doc_completion < 0.5:
        factors.append("Incomplete documentation (-)")
    if compute_aging_score(lead) > 40:
        factors.append("Lead aging elevated (-)")
    if lead.source.value == "whatsapp_referral":
        factors.append("Referral source boost (+)")
    if not factors:
        factors.append("Baseline profile")
    return factors
