from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/revenue/daily")
def revenue_daily(
    on: date = Query(..., description="Day (UTC date) to sum total_price for"),
    db: Session = Depends(get_db),
):
    return controller.daily_revenue(db, on)


@router.get("/revenue/range")
def revenue_range(
    start: datetime = Query(..., description="Inclusive range start"),
    end: datetime = Query(..., description="Inclusive range end"),
    db: Session = Depends(get_db),
):
    return controller.revenue_between(db, start, end)


@router.get("/track/{tracking_number}", response_model=schema.Order)
def order_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number)


@router.post("/{order_id}/apply-promo", response_model=schema.Order)
def apply_promo(order_id: int, body: schema.ApplyPromoBody, db: Session = Depends(get_db)):
    return controller.apply_promotion(db, order_id, body.code)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(
    start: Optional[datetime] = Query(None, description="Filter orders on or after this instant"),
    end: Optional[datetime] = Query(None, description="Filter orders on or before this instant"),
    db: Session = Depends(get_db),
):
    return controller.read_all(db, start=start, end=end)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
