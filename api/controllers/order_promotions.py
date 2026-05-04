from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from ..models import order_promotions as model
from ..schemas import order_promotions as schema
from ..services.order_totals import recalculate_order_total_safe


def create(db: Session, request: schema.OrderPromotionCreate):
    db_row = model.OrderPromotion(order_id=request.order_id, promotion_id=request.promotion_id)
    try:
        db.add(db_row)
        db.commit()
        db.refresh(db_row)
        recalculate_order_total_safe(db, request.order_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__.get("orig", e)))
    return db_row


def read_all(db: Session):
    return db.query(model.OrderPromotion).all()


def read_one(db: Session, item_id: int):
    item = db.query(model.OrderPromotion).filter(model.OrderPromotion.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order promotion not found")
    return item


def update(db: Session, item_id: int, request: schema.OrderPromotionUpdate):
    row = db.query(model.OrderPromotion).filter(model.OrderPromotion.id == item_id)
    existing = row.first()
    if not existing:
        raise HTTPException(status_code=404, detail="Order promotion not found")
    update_data = request.model_dump(exclude_unset=True)
    row.update(update_data, synchronize_session=False)
    db.commit()
    oid = existing.order_id
    recalculate_order_total_safe(db, oid)
    return row.first()


def delete(db: Session, item_id: int):
    row = db.query(model.OrderPromotion).filter(model.OrderPromotion.id == item_id)
    existing = row.first()
    if not existing:
        raise HTTPException(status_code=404, detail="Order promotion not found")
    oid = existing.order_id
    row.delete(synchronize_session=False)
    db.commit()
    recalculate_order_total_safe(db, oid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
