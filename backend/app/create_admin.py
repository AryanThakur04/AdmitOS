"""Create or update admin user. Run inside Docker:
  docker compose exec -e ADMIN_EMAIL=you@gmail.com -e ADMIN_PASSWORD=YourPass -e ADMIN_NAME="Your Name" api python -m app.create_admin
"""
import os
from app.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.services.auth import hash_password


def main():
    email = os.environ.get("ADMIN_EMAIL", "").strip()
    password = os.environ.get("ADMIN_PASSWORD", "").strip()
    name = os.environ.get("ADMIN_NAME", "Admin").strip()

    if not email or not password:
        print("ERROR: Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables.")
        print('Example: docker compose exec -e ADMIN_EMAIL=you@gmail.com -e ADMIN_PASSWORD=Secret123 api python -m app.create_admin')
        return

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        hashed = hash_password(password)
        if user:
            user.hashed_password = hashed
            user.full_name = name
            user.role = UserRole.ADMIN
            db.commit()
            print(f"SUCCESS: Updated user {email}")
        else:
            db.add(
                User(
                    email=email,
                    full_name=name,
                    hashed_password=hashed,
                    role=UserRole.ADMIN,
                )
            )
            db.commit()
            print(f"SUCCESS: Created admin {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
