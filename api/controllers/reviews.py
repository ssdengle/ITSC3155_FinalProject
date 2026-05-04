from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from ..models import reviews as model
from ..models.sandwiches import Sandwich
from ..schemas import reviews as schema


def create(db: Session, request: schema.ReviewCreate):
    if not 1 <= request.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    if request.customer_id is None and not (request.guest_name and request.guest_name.strip()):
        raise HTTPException(
            status_code=400,
            detail="Provide either customer_id (registered) or guest_name (no account)",
        )

    db_row = model.Review(
        customer_id=request.customer_id,
        guest_name=request.guest_name.strip() if request.guest_name else None,
        sandwich_id=request.sandwich_id,
        rating=request.rating,
        review_text=request.review_text,
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
    return db.query(model.Review).all()


def read_one(db: Session, item_id: int):
    item = db.query(model.Review).filter(model.Review.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Review not found")
    return item


def update(db: Session, item_id: int, request: schema.ReviewUpdate):
    row = db.query(model.Review).filter(model.Review.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Review not found")
    update_data = request.model_dump(exclude_unset=True)
    if "guest_name" in update_data and update_data["guest_name"] is not None:
        update_data["guest_name"] = update_data["guest_name"].strip()
    row.update(update_data, synchronize_session=False)
    db.commit()
    return row.first()


def delete(db: Session, item_id: int):
    row = db.query(model.Review).filter(model.Review.id == item_id)
    if not row.first():
        raise HTTPException(status_code=404, detail="Review not found")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def low_rated_dishes(db: Session, threshold: float = 3.0):
    """Average rating at or below threshold (popularity / quality signal for staff)."""
    rows = (
        db.query(
            model.Review.sandwich_id,
            Sandwich.sandwich_name,
            func.avg(model.Review.rating).label("avg_rating"),
            func.count(model.Review.id).label("review_count"),
        )
        .join(Sandwich, model.Review.sandwich_id == Sandwich.id)
        .group_by(model.Review.sandwich_id, Sandwich.sandwich_name)
        .having(func.avg(model.Review.rating) <= threshold)
        .order_by(func.avg(model.Review.rating).asc())
        .all()
    )
    return [
        {
            "sandwich_id": r.sandwich_id,
            "sandwich_name": r.sandwich_name,
            "avg_rating": float(r.avg_rating),
            "review_count": int(r.review_count),
        }
        for r in rows
    ]


def complaint_reviews(db: Session, max_rating: int = 2):
    """Reviews at or below max_rating — read review_text for dissatisfaction reasons."""
    return (
        db.query(model.Review)
        .filter(model.Review.rating <= max_rating)
        .order_by(model.Review.id.desc())
        .all()
    )
