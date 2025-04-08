from models.base import BaseModel
from typing import Optional

class Login(BaseModel):
    login_id: int
    username: str
    password_hash: str
    user_type: str
    user_id: int
    created_at: str
    last_login: Optional[str] = None