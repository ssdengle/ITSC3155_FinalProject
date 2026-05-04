from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from ..models import sandwiches as model
from ..schemas import sandwiches as schema


def create(db: Session, request: schema.SandwichCreate):
    db_sandwich = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        tags=request.tags,
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    return db.query(model.Sandwich).all()


def read_one(db: Session, sandwich_id: int):
    item = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return item


def update(db: Session, sandwich_id: int, request: schema.SandwichUpdate):
    db_sandwich = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")

    update_data = request.model_dump(exclude_unset=True)  # Pydantic v2 syntax
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()


def search_by_tag(db: Session, tag: str):
    q = tag.strip().lower()
    if not q:
        return []
    return (
        db.query(model.Sandwich)
        .filter(
            or_(
                model.Sandwich.sandwich_name.ilike(f"%{q}%"),
                and_(model.Sandwich.tags.isnot(None), model.Sandwich.tags.ilike(f"%{q}%")),
            )
        )
        .all()
    )


def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)