from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from ..models import recipes as model
from ..schemas import recipes as schema


def create(db: Session, request: schema.RecipeCreate):
    db_row = model.Recipe(
        sandwich_id=request.sandwich_id,
        resource_id=request.resource_id,
        amount=request.amount,
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
    return db.query(model.Recipe).all()


def read_one(db: Session, item_id: int):
    item = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return item


def update(db: Session, item_id: int, request: schema.RecipeUpdate):
    row = db.query(model.Recipe).filter(model.Recipe.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = request.model_dump(exclude_unset=True)
    row.update(update_data, synchronize_session=False)
    db.commit()
    return row.first()


def delete(db: Session, item_id: int):
    row = db.query(model.Recipe).filter(model.Recipe.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Recipe not found")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
