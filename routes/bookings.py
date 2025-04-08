from fastapi import APIRouter, Depends, HTTPException
from services.booking_service import BookingService
from models.booking import BookingRequest, Booking
from routes.auth import get_current_user, get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Booking])
async def get_bookings(user=Depends(get_current_admin)):
    return BookingService.get_all_bookings()

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int, user=Depends(get_current_admin)):
    try:
        return BookingService.get_booking(booking_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Booking, status_code=201)
async def book_tickets(booking: BookingRequest, user=Depends(get_current_user)):
    if user["user_type"] != "CUSTOMER":
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        return BookingService.book_tickets(booking, user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/customer/{customer_id}", response_model=list[Booking])
async def get_bookings_by_customer(customer_id: int, user=Depends(get_current_admin)):
    try:
        return BookingService.get_bookings_by_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{booking_id}")
async def update_booking(booking_id: int, total_amount: float | None = None, payment_method: str | None = None, 
                         status: str | None = None, user=Depends(get_current_admin)):
    try:
        BookingService.update_booking(booking_id, total_amount, payment_method, status, user["user_id"])
        return {"message": "Booking updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user=Depends(get_current_admin)):
    try:
        BookingService.delete_booking(booking_id, user["user_id"])
        return {"message": "Booking deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))