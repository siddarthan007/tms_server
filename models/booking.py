from models.base import BaseModel
from typing import List

class Booking(BaseModel):
    booking_id: int
    customer_id: int
    booking_time: str
    total_amount: float
    payment_method: str
    booking_status: str

class BookingRequest(BaseModel):
    show_id: int
    seat_ids: List[int]
    payment_method: str
    ticket_type: str