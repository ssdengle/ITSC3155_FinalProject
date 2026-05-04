from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from ..models import customers as model
from ..schemas import customers as schema


def create(db: Session, request: schema.CustomerCreate):
    db_row = model.Customer(
        name=request.name,
        email=request.email,
        phone=request.phone,
        address=request.address,
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
    return db.query(model.Customer).all()


def read_one(db: Session, item_id: int):
    item = db.query(model.Customer).filter(model.Customer.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Customer not found")
    return item


def update(db: Session, item_id: int, request: schema.CustomerUpdate):
    row = db.query(model.Customer).filter(model.Customer.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Customer not found")
    update_data = request.model_dump(exclude_unset=True)
    row.update(update_data, synchronize_session=False)
    db.commit()
    return row.first()


def delete(db: Session, item_id: int):
    row = db.query(model.Customer).filter(model.Customer.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Customer not found")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
