from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine, get_db

# Buat tabel database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items API")

# ENDPOINT 1: GET semua items
@app.get("/items/", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# ENDPOINT 2: GET item by ID
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# ENDPOINT 3: POST (untuk nambah data biar bisa di-GET)
@app.post("/items/")
def create_item(
    name: str, 
    price: float, 
    description: str = None, 
    is_offer: bool = False, 
    db: Session = Depends(get_db)
):
    db_item = models.Item(
        name=name,
        description=description,
        price=price,
        is_offer=is_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item created", "id": db_item.id}