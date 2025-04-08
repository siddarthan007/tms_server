from repositories.base_repository import BaseRepository
from models.audit_log import AuditLog

class AuditLogRepository(BaseRepository):
    def create(self, admin_id: int, action: str, entity_type: str, entity_id: int | None, details: str | None) -> int:
        self.cursor.execute(
            "INSERT INTO AUDIT_LOG (admin_id, action, entity_type, entity_id, details) VALUES (?, ?, ?, ?, ?)",
            (admin_id, action, entity_type, entity_id, details)
        )
        return self.cursor.lastrowid

    def get_all(self) -> list[AuditLog]:
        self.cursor.execute("SELECT * FROM AUDIT_LOG")
        return [AuditLog.model_validate(dict(row)) for row in self.cursor.fetchall()]