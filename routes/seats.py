from fastapi import APIRouter, Depends, HTTPException
from services.seat_service import SeatService
from models.seat import Seat, SeatCreate, SeatUpdate
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Seat])
async def get_seats(user=Depends(get_current_admin)):
    return SeatService.get_all_seats()

@router.get("/{seat_id}", response_model=Seat)
async def get_seat(seat_id: int, user=Depends(get_current_admin)):
    try:
        return SeatService.get_seat(seat_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/available/{show_id}", response_model=list[Seat])
async def get_available_seats(show_id: int):
    return SeatService.get_available_seats(show_id)

@router.get("/layout/{layout_id}", response_model=list[Seat])
async def get_seats_by_layout(layout_id: int):
    try:
        return SeatService.get_seats_by_layout(layout_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=201)
async def create_seat(seat: SeatCreate, user=Depends(get_current_admin)):
    try:
        seat_id = SeatService.create_seat(seat, user["user_id"])
        return {"message": "Seat created", "seat_id": seat_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{seat_id}")
async def update_seat(seat_id: int, update: SeatUpdate, user=Depends(get_current_admin)):
    try:
        SeatService.update_seat(seat_id, update, user["user_id"])
        return {"message": "Seat updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{seat_id}")
async def delete_seat(seat_id: int, user=Depends(get_current_admin)):
    try:
        SeatService.delete_seat(seat_id, user["user_id"])
        return {"message": "Seat deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))