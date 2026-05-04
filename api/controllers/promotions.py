from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from ..models import promotions as model
from ..schemas import promotions as schema


def create(db: Session, request: schema.PromotionCreate):
    db_row = model.Promotion(
        code=request.code.strip(),
        expiration_date=request.expiration_date,
        discount_value=request.discount_value,
    )
    try:
        db.add(db_row)
        db.commit()
        db.refresh(db_row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__.get("orig", e)))
    return db_row


def read_all(db: Session):
    return db.query(model.Promotion).all()


def read_one(db: Session, item_id: int):
    item = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return item


def update(db: Session, item_id: int, request: schema.PromotionUpdate):
    row = db.query(model.Promotion).filter(model.Promotion.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Promotion not found")
    update_data = request.model_dump(exclude_unset=True)
    if "code" in update_data and update_data["code"] is not None:
        update_data["code"] = update_data["code"].strip()
    row.update(update_data, synchronize_session=False)
    db.commit()
    return row.first()


def delete(db: Session, item_id: int):
    row = db.query(model.Promotion).filter(model.Promotion.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Promotion not found")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
