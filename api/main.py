from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies.database import engine, Base, get_db
from api.models import models
from api.models.schemas import (
    Sandwich, SandwichCreate, SandwichUpdate,
    Resource, ResourceCreate, ResourceUpdate
)
from api.controllers import sandwiches, resources

# Create database tables (auto-run)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QuickPlate API",
    description="Online Restaurant Ordering System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "QuickPlate API is running! Go to /docs for documentation"}

# ============ Sandwiches Endpoints ============
@app.post("/sandwiches/", response_model=Sandwich, tags=["Sandwiches"])
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)

@app.get("/sandwiches/", response_model=list[Sandwich], tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.get("/sandwiches/{sandwich_id}", response_model=Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

@app.put("/sandwiches/{sandwich_id}", response_model=Sandwich, tags=["Sandwiches"])
def update_one_sandwich(sandwich_id: int, sandwich: SandwichUpdate, db: Session = Depends(get_db)):
    existing = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwiches.update(db=db, sandwich=sandwich, sandwich_id=sandwich_id)

@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    existing = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwiches.delete(db=db, sandwich_id=sandwich_id)

# ============ Resources Endpoints ============
@app.post("/resources/", response_model=Resource, tags=["Resources"])
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(db=db, resource=resource)

@app.get("/resources/", response_model=list[Resource], tags=["Resources"])
def read_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

@app.get("/resources/{resource_id}", response_model=Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.put("/resources/{resource_id}", response_model=Resource, tags=["Resources"])
def update_one_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)):
    existing = resources.read_one(db, resource_id=resource_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resources.update(db=db, resource=resource, resource_id=resource_id)

@app.delete("/resources/{resource_id}", tags=["Resources"])
def delete_one_resource(resource_id: int, db: Session = Depends(get_db)):
    existing = resources.read_one(db, resource_id=resource_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resources.delete(db=db, resource_id=resource_id)