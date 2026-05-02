from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail] = []

    class Config:
        orm_mode = True