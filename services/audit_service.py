from database.connection import get_db
from repositories.audit_log_repository import AuditLogRepository

class AuditService:
    @staticmethod
    def log_action(admin_id: int, action: str, entity_type: str, entity_id: int | None, details: str | None):
        with get_db() as conn:
            repo = AuditLogRepository(conn)
            repo.create(admin_id, action, entity_type, entity_id, details)
            repo.commit()