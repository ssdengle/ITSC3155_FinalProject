from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..dependencies.database import get_db

router = APIRouter(tags=["Reviews"], prefix="/reviews")


@router.get("/analytics/low-rated")
def analytics_low_rated(
    threshold: float = Query(default=3.0, ge=1.0, le=5.0),
    db: Session = Depends(get_db),
) -> List[dict[str, Any]]:
    return controller.low_rated_dishes(db, threshold=threshold)


@router.get("/analytics/complaints", response_model=list[schema.Review])
def analytics_complaints(
    max_rating: int = Query(default=2, ge=1, le=5),
    db: Session = Depends(get_db),
):
    return controller.complaint_reviews(db, max_rating=max_rating)


@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Review])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Review)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Review)
def update(item_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
