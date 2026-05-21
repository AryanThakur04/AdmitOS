import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token, UserResponse
from app.services.auth import verify_password, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()
    except SQLAlchemyError as e:
        logger.exception("Database error during login")
        raise HTTPException(
            status_code=503,
            detail="Database unavailable. Run: docker compose up -d",
        ) from e

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        token = create_access_token(user.email)
    except Exception as e:
        logger.exception("Token creation failed")
        raise HTTPException(status_code=500, detail="Could not create token") from e

    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
    )
