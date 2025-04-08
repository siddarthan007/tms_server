from models.base import BaseModel
from typing import Optional

class Show(BaseModel):
    show_id: int
    movie_id: int
    screen_id: int
    show_time: str
    ticket_price: float
    status: str
    theatre_name: Optional[str] = None
    screen_name: Optional[str] = None

class ShowCreate(BaseModel):
    movie_id: int
    screen_id: int
    show_time: str
    ticket_price: float
    status: str = "ACTIVE"

class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    screen_id: Optional[int] = None
    show_time: Optional[str] = None
    ticket_price: Optional[float] = None
    status: Optional[str] = None