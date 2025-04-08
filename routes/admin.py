from fastapi import APIRouter, Depends, HTTPException, status
from services.admin_service import AdminService
from models.admin import Admin, AdminCreate
from routes.auth import get_current_admin

router = APIRouter(prefix="/admins", tags=["admins"])

@router.get("/", response_model=list[Admin])
async def get_admins(user=Depends(get_current_admin)):
    return AdminService.get_all_admins()

@router.get("/{admin_id}", response_model=Admin)
async def get_admin(admin_id: int, user=Depends(get_current_admin)):
    try:
        return AdminService.get_admin(admin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminCreate, user=Depends(get_current_admin)):
    try:
        admin_id = AdminService.create_admin(admin, user["user_id"])
        return {"message": "Admin created", "admin_id": admin_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{admin_id}")
async def update_admin(admin_id: int, name: str | None = None, email: str | None = None, 
                      phone_number: str | None = None, role: str | None = None, user=Depends(get_current_admin)):
    try:
        AdminService.update_admin(admin_id, name, email, phone_number, role, user["user_id"])
        return {"message": "Admin updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{admin_id}")
async def delete_admin(admin_id: int, user=Depends(get_current_admin)):
    try:
        AdminService.delete_admin(admin_id, user["user_id"])
        return {"message": "Admin deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))