from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, session
from app.schemas import Stock

router = APIRouter()

# Dependency


def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stocks", response_model=list[Stock])
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(models.Stock).all()
    return stocks


@router.post("/stocks", response_model=Stock)
def add_stock(stock_data: Stock, db: Session = Depends(get_db)):
    db_stock = db.query(models.Stock).filter(
        models.Stock.symbol == stock_data.symbol).first()
    if db_stock:
        raise HTTPException(status_code=400, detail="Stock already exists")
    db.add(stock_data)
    db.commit()
    db.refresh(stock_data)
    return stock_data
