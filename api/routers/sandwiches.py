from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Sandwiches'],
    prefix="/sandwiches"
)


@router.get("/search", response_model=list[schema.Sandwich])
def search_sandwiches(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Find menu items by tag (e.g. vegetarian) or name substring."""
    return controller.search_by_tag(db, q)


@router.post("/", response_model=schema.Sandwich)
def create(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Sandwich])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{sandwich_id}", response_model=schema.Sandwich)
def read_one(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, sandwich_id=sandwich_id)


@router.put("/{sandwich_id}", response_model=schema.Sandwich)
def update(sandwich_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, sandwich_id=sandwich_id)


@router.delete("/{sandwich_id}")
def delete(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, sandwich_id=sandwich_id)