import itertools

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Demo CRUD API", description="A demo FastAPI CRUD application", version="1.0.0")

# In-memory storage
db: dict[int, dict] = {}
_id_counter = itertools.count(1)


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool


@app.get("/items", response_model=list[Item])
def list_items():
    """Return all items."""
    return list(db.values())


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    """Create a new item."""
    item_id = next(_id_counter)
    new_item = {"id": item_id, **item.model_dump()}
    db[item_id] = new_item
    return new_item


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Retrieve a single item by ID."""
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item."""
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored = db[item_id]
    updates = item.model_dump(exclude_unset=True)
    stored.update(updates)
    db[item_id] = stored
    return stored


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
