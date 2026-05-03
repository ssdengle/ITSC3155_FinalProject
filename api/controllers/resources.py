from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from ..models import resources as model
from ..schemas import resources as schema


def create(db: Session, request: schema.ResourceCreate):
    db_resource = model.Resource(
        item=request.item,
        amount=request.amount
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def read_all(db: Session):
    return db.query(model.Resource).all()


def read_one(db: Session, resource_id: int):
    item = db.query(model.Resource).filter(model.Resource.id == resource_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item


def update(db: Session, resource_id: int, request: schema.ResourceUpdate):
    db_resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=404, detail="Resource not found")

    update_data = request.model_dump(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()


def delete(db: Session, resource_id: int):
    db_resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
    if not db_resource.first():
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)