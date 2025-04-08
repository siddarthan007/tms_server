from fastapi import APIRouter, Depends, HTTPException
from services.theatre_service import TheatreService
from models.theatre import Theatre
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Theatre])
async def get_theatres():
    return TheatreService.get_all_theatres()

@router.get("/{theatre_id}", response_model=Theatre)
async def get_theatre(theatre_id: int):
    try:
        return TheatreService.get_theatre(theatre_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=201)
async def create_theatre(name: str, location: str | None = None, contact_number: str | None = None, 
                         user=Depends(get_current_admin)):
    try:
        theatre_id = TheatreService.create_theatre(name, location, contact_number, user["user_id"])
        return {"message": "Theatre created", "theatre_id": theatre_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{theatre_id}")
async def update_theatre(theatre_id: int, name: str | None = None, location: str | None = None, 
                         contact_number: str | None = None, user=Depends(get_current_admin)):
    try:
        TheatreService.update_theatre(theatre_id, name, location, contact_number, user["user_id"])
        return {"message": "Theatre updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{theatre_id}")
async def delete_theatre(theatre_id: int, user=Depends(get_current_admin)):
    try:
        TheatreService.delete_theatre(theatre_id, user["user_id"])
        return {"message": "Theatre deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))