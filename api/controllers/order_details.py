from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import order_details as model
from ..services import inventory
from ..services.order_totals import recalculate_order_total_safe


def create(db: Session, request):
    try:
        inventory.deduct_for_line(db, request.sandwich_id, request.amount)
        new_item = model.OrderDetail(
            order_id=request.order_id,
            sandwich_id=request.sandwich_id,
            amount=request.amount,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        recalculate_order_total_safe(db, request.order_id)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    old = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    if not old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    try:
        inventory.restore_for_line(db, old.sandwich_id, old.amount)

        new_sid = request.sandwich_id if request.sandwich_id is not None else old.sandwich_id
        new_amt = request.amount if request.amount is not None else old.amount

        inventory.deduct_for_line(db, new_sid, new_amt)

        update_data = request.model_dump(exclude_unset=True)
        item_q = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        item_q.update(update_data, synchronize_session=False)
        db.commit()
        recalculate_order_total_safe(db, old.order_id)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return read_one(db, item_id)


def delete(db: Session, item_id):
    old = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    if not old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

    oid = old.order_id
    try:
        inventory.restore_for_line(db, old.sandwich_id, old.amount)
        db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).delete(synchronize_session=False)
        db.commit()
        recalculate_order_total_safe(db, oid)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
