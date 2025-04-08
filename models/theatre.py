from models.base import BaseModel
from typing import Optional

class Theatre(BaseModel):
    theatre_id: int
    name: str
    location: Optional[str] = None
    contact_number: Optional[str] = None
    created_at: str