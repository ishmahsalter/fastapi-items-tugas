from pydantic import BaseModel
from typing import Optional

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool

    class Config:
        from_attributes = True