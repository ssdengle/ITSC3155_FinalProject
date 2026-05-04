from typing import Optional
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    order_id: Optional[int] = None
    payment_type: Optional[str] = None
    card_number: Optional[str] = None
    transaction_status: Optional[str] = None


class PaymentCreate(PaymentBase):
    order_id: int
    payment_type: str
    transaction_status: str


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    payment_type: Optional[str] = None
    card_number: Optional[str] = None
    transaction_status: Optional[str] = None


class Payment(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
