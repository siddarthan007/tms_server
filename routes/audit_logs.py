from fastapi import APIRouter, Depends
from repositories.audit_log_repository import AuditLogRepository
from database.connection import get_db
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list)
async def get_audit_logs(user=Depends(get_current_admin), conn=Depends(get_db)):
    repo = AuditLogRepository(conn)
    return repo.get_all()