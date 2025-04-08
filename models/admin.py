from models.base import BaseModel
from typing import Optional

class Admin(BaseModel):
    admin_id: int
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role: str
    created_at: str

class AdminCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    role: str = "Manager"
    username: str
    password: str