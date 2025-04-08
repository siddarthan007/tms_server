from fastapi import APIRouter, Depends, HTTPException
from services.ticket_service import TicketService
from models.ticket import Ticket, TicketCreate, TicketUpdate
from routes.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[Ticket])
async def get_tickets(user=Depends(get_current_admin)):
    return TicketService.get_all_tickets()

@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int, user=Depends(get_current_admin)):
    try:
        return TicketService.get_ticket(ticket_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/booking/{booking_id}", response_model=list[Ticket])
async def get_tickets_by_booking(booking_id: int, user=Depends(get_current_admin)): 
    try:
        return TicketService.get_tickets_by_booking(booking_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/show/{show_id}", response_model=list[Ticket])
async def get_tickets_by_show(show_id: int, user=Depends(get_current_admin)):
    try:
        return TicketService.get_tickets_by_show(show_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", status_code=201)
async def create_ticket(ticket: TicketCreate, user=Depends(get_current_admin)):
    try:
        ticket_id = TicketService.create_ticket(ticket, user["user_id"])
        return {"message": "Ticket created", "ticket_id": ticket_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{ticket_id}")
async def update_ticket(ticket_id: int, update: TicketUpdate, user=Depends(get_current_admin)):
    try:
        TicketService.update_ticket(ticket_id, update, user["user_id"])
        return {"message": "Ticket updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, user=Depends(get_current_admin)):
    try:
        TicketService.delete_ticket(ticket_id, user["user_id"])
        return {"message": "Ticket deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))