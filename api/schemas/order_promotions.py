from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrderPromotionBase(BaseModel):
    order_id: Optional[int] = None
    promotion_id: Optional[int] = None


class OrderPromotionCreate(OrderPromotionBase):
    order_id: int
    promotion_id: int


class OrderPromotionUpdate(BaseModel):
    order_id: Optional[int] = None
    promotion_id: Optional[int] = None


class OrderPromotion(OrderPromotionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
