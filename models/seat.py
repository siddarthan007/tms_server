from models.base import BaseModel
from typing import Optional

class Seat(BaseModel):
    seat_id: int
    layout_id: int
    row_label: str
    seat_number: str
    seat_category: str
    is_accessible: int
    price: float
    status: str

class SeatCreate(BaseModel):
    layout_id: int
    row_label: str
    seat_number: str
    seat_category: str = "Standard"
    is_accessible: int = 0
    price: float
    status: str = "AVAILABLE"

class SeatUpdate(BaseModel):
    row_label: Optional[str] = None
    seat_number: Optional[str] = None
    seat_category: Optional[str] = None
    is_accessible: Optional[int] = None
    price: Optional[float] = None
    status: Optional[str] = None