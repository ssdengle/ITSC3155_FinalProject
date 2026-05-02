from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class OrderPromotion(Base):
    __tablename__ = "order_promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=False, index=True)

    order = relationship("Order", back_populates="order_promotions")
    promotion = relationship("Promotion", back_populates="order_promotions")
