from fastapi import APIRouter, Depends, HTTPException
from services.screen_service import ScreenService
from models.screen import Screen, ScreenCreate
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Screen])
async def get_screens():
    return ScreenService.get_all_screens()

@router.get("/{screen_id}", response_model=Screen)
async def get_screen(screen_id: int):
    try:
        return ScreenService.get_screen(screen_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=201)
async def add_screen(screen: ScreenCreate, user=Depends(get_current_admin)):
    try:
        screen_id = ScreenService.add_screen(screen, user["user_id"])
        return {"message": "Screen added", "screen_id": screen_id}
    except Exception:
        raise HTTPException(status_code=400, detail="Screen addition failed")

@router.get("/theatre/{theatre_id}", response_model=list[Screen])
async def get_screens_by_theatre(theatre_id: int):
    try:
        return ScreenService.get_screens_by_theatre(theatre_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{screen_id}")
async def update_screen(screen_id: int, theatre_id: int | None = None, screen_name: str | None = None, 
                       capacity: int | None = None, user=Depends(get_current_admin)):
    try:
        ScreenService.update_screen(screen_id, theatre_id, screen_name, capacity, user["user_id"])
        return {"message": "Screen updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{screen_id}")
async def delete_screen(screen_id: int, user=Depends(get_current_admin)):
    try:
        ScreenService.delete_screen(screen_id, user["user_id"])
        return {"message": "Screen deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))