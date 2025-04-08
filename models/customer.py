from models.base import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: str

class CustomerRegister(BaseModel):
    name: str
    email: str
    phone_number: str
    username: str
    password: str