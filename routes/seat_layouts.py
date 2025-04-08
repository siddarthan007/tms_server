from fastapi import APIRouter, Depends, HTTPException
from services.seat_layout_service import SeatLayoutService
from models.seat_layout import SeatLayout, SeatLayoutCreate, SeatLayoutUpdate
from routes.auth import get_current_admin

router = APIRouter()

@router.post("/", status_code=201)
async def create_seat_layout(seat_layout: SeatLayoutCreate, user=Depends(get_current_admin)):
    try:
        layout_id = SeatLayoutService.create_seat_layout(seat_layout, user["user_id"])
        return {"message": "Seat layout created", "layout_id": layout_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{layout_id}", response_model=SeatLayout)
async def get_seat_layout(layout_id: int, user=Depends(get_current_admin)):
    try:
        return SeatLayoutService.get_seat_layout(layout_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/", response_model=list[SeatLayout])
async def get_all_seat_layouts(user=Depends(get_current_admin)):
    return SeatLayoutService.get_all_seat_layouts()

@router.get("/screen/{screen_id}", response_model=list[SeatLayout])
async def get_seat_layouts_by_screen(screen_id: int, user=Depends(get_current_admin)):
    return SeatLayoutService.get_seat_layouts_by_screen(screen_id)

@router.put("/{layout_id}")
async def update_seat_layout(layout_id: int, update: SeatLayoutUpdate, user=Depends(get_current_admin)):
    try:
        SeatLayoutService.update_seat_layout(layout_id, update, user["user_id"])
        return {"message": "Seat layout updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{layout_id}")
async def delete_seat_layout(layout_id: int, user=Depends(get_current_admin)):
    try:
        SeatLayoutService.delete_seat_layout(layout_id, user["user_id"])
        return {"message": "Seat layout deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))