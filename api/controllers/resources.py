from sqlalchemy.orm import Session
from fastapi import Response, status
from api.models import models
from api.models.schemas import ResourceCreate, ResourceUpdate

def create(db: Session, resource: ResourceCreate):
    db_resource = models.Resource(
        name=resource.name,
        unit=resource.unit,
        quantity_in_stock=resource.quantity_in_stock
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def update(db: Session, resource_id: int, resource: ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    update_data = resource.dict(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()

def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)