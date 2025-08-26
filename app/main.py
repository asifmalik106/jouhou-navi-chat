from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="FastAPI Lambda API")

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# In-memory storage
items = {}

@app.get("/")
def root():
    return {"message": "FastAPI on Lambda"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/items")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item.dict()
    return {"id": item_id, **item.dict()}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id]}

@app.get("/items")
def list_items():
    return [{"id": id, **item} for id, item in items.items()]