from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import order_promotions as controller
from ..schemas import order_promotions as schema
from ..dependencies.database import get_db

router = APIRouter(tags=["Order Promotions"], prefix="/order-promotions")


@router.post("/", response_model=schema.OrderPromotion)
def create(request: schema.OrderPromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.OrderPromotion])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.OrderPromotion)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.OrderPromotion)
def update(item_id: int, request: schema.OrderPromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
