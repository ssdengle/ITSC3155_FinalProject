"""Compute order subtotals, promotional discounts, and persisted totals."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from ..models.order_details import OrderDetail
from ..models.order_promotions import OrderPromotion
from ..models.orders import Order
from ..models.promotions import Promotion


def _decimal_price(val) -> Decimal:
    if val is None:
        return Decimal("0")
    return Decimal(str(val))


def recalculate_order_total_safe(db: Session, order_id: int) -> Order | None:
    """Recompute and persist total_price from line items and valid promotions."""
    order = (
        db.query(Order)
        .options(
            joinedload(Order.order_details).joinedload(OrderDetail.sandwich),
            joinedload(Order.order_promotions).joinedload(OrderPromotion.promotion),
        )
        .filter(Order.id == order_id)
        .first()
    )
    if order is None:
        return None

    subtotal = Decimal("0")
    for detail in order.order_details:
        sw = detail.sandwich
        price = _decimal_price(sw.price if sw else None)
        subtotal += price * int(detail.amount)

    discount = Decimal("0")
    today = date.today()
    for op in order.order_promotions:
        prom: Promotion | None = op.promotion
        if prom is None or prom.expiration_date < today:
            continue
        pct = _decimal_price(prom.discount_value)
        disc_amt = (subtotal * pct / Decimal("100")).quantize(Decimal("0.01"))
        if disc_amt > discount:
            discount = disc_amt

    total = (subtotal - discount).quantize(Decimal("0.01"))
    if total < 0:
        total = Decimal("0")

    order.total_price = total
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
