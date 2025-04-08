from models.base import BaseModel
from typing import Optional

class SeatLayout(BaseModel):
    layout_id: int
    screen_id: int
    layout_name: Optional[str] = None
    layout_type: str
    total_rows: int
    total_columns: int
    created_at: str

class SeatLayoutCreate(BaseModel):
    screen_id: int
    layout_name: Optional[str] = None
    layout_type: str
    total_rows: int
    total_columns: int

class SeatLayoutUpdate(BaseModel):
    layout_name: Optional[str] = None
    layout_type: Optional[str] = None
    total_rows: Optional[int] = None
    total_columns: Optional[int] = None