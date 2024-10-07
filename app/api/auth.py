from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import models, session
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.utils import hash_password, verify_password, create_access_token, verify_access_token
# from datetime import timedelta

router = APIRouter()

# Dependency


def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username,
                          email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # select *
    # from users
    # where users.email = 'sdjfh@jshd.sdj'
    # limit 1

    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=UserResponse)
def token(payload: dict, db: Session = Depends(get_db)):
    # This endpoint is used to verify the JWT token
    user_data = verify_access_token(payload["token"])
    db_user = db.query(models.User).filter(
        models.User.email == user_data["sub"]).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
