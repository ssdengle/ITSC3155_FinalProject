from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ============ Sandwich Schemas ============
class SandwichBase(BaseModel):
    name: str
    price: float
    size: Optional[str] = None
    ingredients: Optional[str] = None


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    size: Optional[str] = None
    ingredients: Optional[str] = None


class Sandwich(SandwichBase):
    id: int

    class Config:
        from_attributes = True


# ============ Resource Schemas ============
class ResourceBase(BaseModel):
    name: str
    unit: str
    quantity_in_stock: int


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    quantity_in_stock: Optional[int] = None


class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True


# ============ Recipe Schemas ============
class RecipeBase(BaseModel):
    sandwich_id: int
    resource_id: int
    quantity_required: float


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    quantity_required: Optional[float] = None


class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True


# ============ Order Schemas ============
class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True


# ============ OrderDetail Schemas ============
class OrderDetailBase(BaseModel):
    order_id: int
    sandwich_id: int
    quantity: int


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    quantity: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int

    class Config:
        from_attributes = True