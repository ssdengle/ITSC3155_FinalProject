import secrets
from datetime import date, datetime, time, timedelta
from typing import Optional

from fastapi import HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from ..models import orders as model
from ..models.order_details import OrderDetail
from ..models.order_promotions import OrderPromotion
from ..models.payments import Payment
from ..models.promotions import Promotion
from ..services.order_totals import recalculate_order_total_safe


def _make_tracking_number(db: Session) -> str:
    for _ in range(30):
        t = secrets.token_hex(5).upper()
        if not db.query(model.Order).filter(model.Order.tracking_number == t).first():
            return t
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not generate unique tracking number",
    )


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        customer_id=request.customer_id,
        order_type=getattr(request, "order_type", None) or "takeout",
        order_status=getattr(request, "order_status", None) or "pending",
        tracking_number=_make_tracking_number(db),
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return read_one(db, new_item.id)


def read_all(
    db: Session,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    try:
        q = db.query(model.Order).options(
            joinedload(model.Order.order_details).joinedload(OrderDetail.sandwich)
        )
        if start is not None:
            q = q.filter(model.Order.order_date >= start)
        if end is not None:
            q = q.filter(model.Order.order_date <= end)
        return q.order_by(model.Order.order_date.desc()).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = (
            db.query(model.Order)
            .options(joinedload(model.Order.order_details).joinedload(OrderDetail.sandwich))
            .filter(model.Order.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_tracking(db: Session, tracking_number: str):
    q = tracking_number.strip().upper()
    item = (
        db.query(model.Order)
        .options(joinedload(model.Order.order_details).joinedload(OrderDetail.sandwich))
        .filter(model.Order.tracking_number.isnot(None))
        .filter(func.upper(model.Order.tracking_number) == q)
        .first()
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found")
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.model_dump(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return read_one(db, item_id)


def delete(db: Session, item_id):
    from ..services import inventory

    details = db.query(OrderDetail).filter(OrderDetail.order_id == item_id).all()
    try:
        for d in details:
            inventory.restore_for_line(db, d.sandwich_id, d.amount)
        db.query(OrderPromotion).filter(OrderPromotion.order_id == item_id).delete(synchronize_session=False)
        db.query(Payment).filter(Payment.order_id == item_id).delete(synchronize_session=False)
        db.query(OrderDetail).filter(OrderDetail.order_id == item_id).delete(synchronize_session=False)
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def daily_revenue(db: Session, on: date):
    start = datetime.combine(on, time.min)
    end = start + timedelta(days=1)
    total = (
        db.query(func.coalesce(func.sum(model.Order.total_price), 0))
        .filter(model.Order.order_date >= start, model.Order.order_date < end)
        .scalar()
    )
    return {"date": on.isoformat(), "revenue": float(total) if total is not None else 0.0}


def revenue_between(db: Session, start: datetime, end: datetime):
    total = (
        db.query(func.coalesce(func.sum(model.Order.total_price), 0))
        .filter(model.Order.order_date >= start, model.Order.order_date <= end)
        .scalar()
    )
    return {"start": start.isoformat(), "end": end.isoformat(), "revenue": float(total) if total else 0.0}


def apply_promotion(db: Session, order_id: int, code: str):
    order = db.query(model.Order).filter(model.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    prom = db.query(Promotion).filter(Promotion.code == code.strip()).first()
    if not prom:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid promotion code")
    if prom.expiration_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code has expired")

    db.query(OrderPromotion).filter(OrderPromotion.order_id == order_id).delete(synchronize_session=False)
    db.add(OrderPromotion(order_id=order_id, promotion_id=prom.id))
    db.commit()

    recalculate_order_total_safe(db, order_id)
    return read_one(db, order_id)
