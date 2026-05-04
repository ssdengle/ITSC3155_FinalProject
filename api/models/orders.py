from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))

    tracking_number = Column(String(32), unique=True, index=True, nullable=True)
    order_type = Column(String(20), nullable=False, server_default="takeout")
    order_status = Column(String(30), nullable=False, server_default="pending")
    total_price = Column(DECIMAL(10, 2), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    order_promotions = relationship("OrderPromotion", back_populates="order")