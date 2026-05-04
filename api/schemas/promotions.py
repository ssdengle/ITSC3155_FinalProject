from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PromotionBase(BaseModel):
    code: Optional[str] = None
    expiration_date: Optional[date] = None
    discount_value: Optional[float] = None


class PromotionCreate(PromotionBase):
    code: str
    expiration_date: date
    discount_value: float


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    expiration_date: Optional[date] = None
    discount_value: Optional[float] = None


class Promotion(PromotionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
