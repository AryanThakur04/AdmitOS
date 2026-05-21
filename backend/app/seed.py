"""Seed demo users, leads, documents, touchpoints, alerts, referrals."""
from datetime import datetime, timedelta
import random
from app.models.touchpoint import TouchpointType
from app.database import SessionLocal, Base, engine
from app.models import *
from app.models.user import UserRole
from app.services.auth import hash_password
from app.services.risk_detector import scan_all_leads

NAMES = [
    ("Aisha Khan", "aisha.k@email.com", "+971501234567", "UAE", "MBA"),
    ("James Okafor", "j.okafor@email.com", "+234801234567", "Nigeria", "Computer Science"),
    ("Priya Sharma", "priya.s@email.com", "+919876543210", "India", "Data Science"),
    ("Lucas Müller", "l.muller@email.com", "+4915123456789", "Germany", "Engineering"),
    ("Sofia Reyes", "sofia.r@email.com", "+5215512345678", "Mexico", "Business Analytics"),
    ("Chen Wei", "chen.w@email.com", "+8613812345678", "China", "Finance"),
    ("Emma Thompson", "emma.t@email.com", "+447911123456", "UK", "Law"),
    ("Omar Hassan", "omar.h@email.com", "+201012345678", "Egypt", "Medicine"),
    ("Yuki Tanaka", "yuki.t@email.com", "+819012345678", "Japan", "Design"),
    ("Maria Santos", "maria.s@email.com", "+5511987654321", "Brazil", "Psychology"),
    ("David Park", "david.p@email.com", "+821012345678", "South Korea", "AI & ML"),
    ("Fatima Al-Rashid", "fatima.a@email.com", "+966501234567", "Saudi Arabia", "Architecture"),
    ("Noah Williams", "noah.w@email.com", "+16135551234", "Canada", "Nursing"),
    ("Ananya Patel", "ananya.p@email.com", "+919988776655", "India", "Biotechnology"),
    ("Carlos Mendez", "carlos.m@email.com", "+34612345678", "Spain", "Hospitality"),
]

SOURCES = [LeadSource.FACEBOOK, LeadSource.WEBSITE, LeadSource.WHATSAPP_REFERRAL, LeadSource.CSV_IMPORT]
STATUSES = [LeadStatus.NEW, LeadStatus.CONTACTED, LeadStatus.QUALIFIED, LeadStatus.APPLICATION, LeadStatus.ACCEPTED, LeadStatus.LOST]
TIERS = [LeadTier.HOT, LeadTier.MEDIUM, LeadTier.COLD]
LOST_REASONS = ["Chose competitor", "Budget constraints", "Visa concerns", "No response", "Program not available", "Changed plans"]
DOC_TYPES = ["Passport Copy", "Academic Transcripts", "Statement of Purpose", "Recommendation Letter", "English Proficiency", "Financial Proof"]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).first():
            print("Database already seeded.")
            return

        admin = User(
            email="admin@admitos.demo",
            full_name="Admin User",
            hashed_password=hash_password("demo1234"),
            role=UserRole.ADMIN,
        )
        priya = User(
            email="priya@admitos.demo",
            full_name="Priya Nair",
            hashed_password=hash_password("demo1234"),
            role=UserRole.COUNSELLOR,
        )
        james = User(
            email="james@admitos.demo",
            full_name="James Mitchell",
            hashed_password=hash_password("demo1234"),
            role=UserRole.COUNSELLOR,
        )
        db.add_all([admin, priya, james])
        db.commit()

        counsellors = [priya, james]
        leads_created = []

        for i, (name, email, phone, country, program) in enumerate(NAMES):
            days_ago = random.randint(1, 45)
            created = datetime.utcnow() - timedelta(days=days_ago)
            last_contact = created + timedelta(days=random.randint(0, min(days_ago, 10)))
            status = random.choice(STATUSES)
            tier = random.choice(TIERS)
            lead = Lead(
                full_name=name,
                email=email,
                phone=phone,
                country=country,
                program_interest=program,
                source=random.choice(SOURCES),
                status=status,
                tier=tier,
                counsellor_id=random.choice(counsellors).id,
                conversion_probability=round(random.uniform(0.15, 0.9), 2),
                aging_score=round(min(100, days_ago * random.uniform(2, 8)), 1),
                lost_reason=random.choice(LOST_REASONS) if status == LeadStatus.LOST else None,
                referral_code=f"REF{1000 + i}" if random.random() > 0.6 else None,
                last_contact_at=last_contact,
                created_at=created,
                updated_at=datetime.utcnow(),
            )
            db.add(lead)
            db.flush()
            leads_created.append(lead)

            for dt in DOC_TYPES:
                st = random.choice(list(DocumentStatus))
                db.add(Document(lead_id=lead.id, doc_type=dt, status=st, is_required=True))

            touchpoints = [
                ("Initial inquiry received", TouchpointType.NOTE, "System"),
                ("WhatsApp intro sent", TouchpointType.WHATSAPP, counsellors[i % 2].full_name),
                ("Discovery call completed", TouchpointType.CALL, counsellors[i % 2].full_name),
            ]
            for j, (title, tp_type, author) in enumerate(touchpoints):
                db.add(
                    Touchpoint(
                        lead_id=lead.id,
                        type=tp_type,
                        title=title,
                        content=f"Automated touchpoint for {name}",
                        created_by=author,
                        created_at=created + timedelta(days=j + 1),
                    )
                )

        # Referral chains
        if len(leads_created) >= 4:
            db.add(
                ReferralChain(
                    referrer_lead_id=leads_created[0].id,
                    referred_lead_id=leads_created[3].id,
                    depth=1,
                    referral_code="REF1000",
                )
            )
            db.add(
                ReferralChain(
                    referrer_lead_id=leads_created[3].id,
                    referred_lead_id=leads_created[7].id,
                    depth=2,
                    referral_code="REF1003",
                )
            )
            leads_created[3].referred_by_lead_id = leads_created[0].id
            leads_created[7].referred_by_lead_id = leads_created[3].id

        db.commit()
        scan_all_leads(db)
        print(f"Seeded {len(leads_created)} leads, 3 users, documents, touchpoints, referrals.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
