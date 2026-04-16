from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    customer_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    customer_id: int
    sandwich_id: int
    rating: int


class ReviewUpdate(BaseModel):
    customer_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
