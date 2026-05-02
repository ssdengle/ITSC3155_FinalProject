from sqlalchemy import Column, Date, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    expiration_date = Column(Date, nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)

    order_promotions = relationship("OrderPromotion", back_populates="promotion")
