from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_type: Optional[str] = None
    order_status: Optional[str] = None


class OrderCreate(BaseModel):
    customer_name: str
    description: Optional[str] = None
    customer_id: Optional[int] = None
    order_type: str = Field(default="takeout", description="takeout or delivery")
    order_status: str = Field(default="pending")


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_type: Optional[str] = None
    order_status: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    total_price: Optional[Decimal] = None
    order_details: List[OrderDetail] = []

    model_config = ConfigDict(from_attributes=True)


class ApplyPromoBody(BaseModel):
    code: str
