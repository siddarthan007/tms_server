from models.base import BaseModel
from typing import Optional

class Ticket(BaseModel):
    ticket_id: int
    show_id: int
    booking_id: int
    seat_id: int
    ticket_type: str

class TicketCreate(BaseModel):
    show_id: int
    booking_id: int
    seat_id: int
    ticket_type: str = "ADULT"

class TicketUpdate(BaseModel):
    show_id: Optional[int] = None
    booking_id: Optional[int] = None
    seat_id: Optional[int] = None
    ticket_type: Optional[str] = None