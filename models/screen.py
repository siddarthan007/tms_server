from models.base import BaseModel

class Screen(BaseModel):
    screen_id: int
    theatre_id: int
    screen_name: str
    capacity: int
    created_at: str

class ScreenCreate(BaseModel):
    theatre_id: int
    screen_name: str
    capacity: int