# Lead Scoring

AdmitOS assigns each lead a **tier** and **conversion probability**.

## Tiers

| Tier | Probability Range |
|------|-------------------|
| Hot | ≥ 65% |
| Medium | 40–64% |
| Cold | < 40% |

## Factors

- Pipeline status (new → accepted)
- Document completion rate
- Lead aging score (inactivity)
- Source boost (WhatsApp referrals +10%)
- Current tier momentum

## Lead Aging Score

0–100 scale. Increases ~8 points per day without contact. Triggers `aging_lead` alerts above 60.

## API

```bash
POST /api/v1/ai/score-lead/1
GET /api/v1/analytics/conversion-prediction/1
```
