from models.base import BaseModel
from typing import Optional

class AuditLog(BaseModel):
    log_id: int
    admin_id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    action_time: str
    details: Optional[str] = None