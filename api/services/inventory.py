"""Recipe-based inventory checks and stock adjustments for order lines."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.recipes import Recipe
from ..models.resources import Resource


def quantities_needed(db: Session, sandwich_id: int, sandwich_qty: int) -> dict[int, int]:
    """resource_id -> units required for sandwich_qty sandwiches."""
    rows = db.query(Recipe).filter(Recipe.sandwich_id == sandwich_id).all()
    need: dict[int, int] = {}
    for r in rows:
        per = int(r.amount)
        need[r.resource_id] = need.get(r.resource_id, 0) + per * sandwich_qty
    return need


def shortage_messages(db: Session, sandwich_id: int, sandwich_qty: int) -> list[str]:
    msgs: list[str] = []
    for rid, units in quantities_needed(db, sandwich_id, sandwich_qty).items():
        res = db.query(Resource).filter(Resource.id == rid).first()
        have = int(res.amount) if res else 0
        label = res.item if res else f"resource#{rid}"
        if have < units:
            msgs.append(f"Insufficient ingredient '{label}': need {units}, have {have}")
    return msgs


def validate_stock(db: Session, sandwich_id: int, sandwich_qty: int) -> tuple[bool, list[str]]:
    msgs = shortage_messages(db, sandwich_id, sandwich_qty)
    return (len(msgs) == 0, msgs)


def deduct_for_line(db: Session, sandwich_id: int, sandwich_qty: int) -> None:
    ok, msgs = validate_stock(db, sandwich_id, sandwich_qty)
    if not ok:
        raise ValueError("; ".join(msgs))
    for rid, units in quantities_needed(db, sandwich_id, sandwich_qty).items():
        res = db.query(Resource).filter(Resource.id == rid).first()
        if res is None:
            raise ValueError(f"Missing inventory row for resource #{rid}")
        res.amount = int(res.amount) - units


def restore_for_line(db: Session, sandwich_id: int, sandwich_qty: int) -> None:
    for rid, units in quantities_needed(db, sandwich_id, sandwich_qty).items():
        res = db.query(Resource).filter(Resource.id == rid).first()
        if res is not None:
            res.amount = int(res.amount) + units
