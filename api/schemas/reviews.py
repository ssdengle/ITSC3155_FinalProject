from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None
    sandwich_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class ReviewCreate(BaseModel):
    sandwich_id: int
    rating: int
    review_text: Optional[str] = None
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None


class ReviewUpdate(BaseModel):
    customer_id: Optional[int] = None
    guest_name: Optional[str] = None
    sandwich_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
