from fastapi import APIRouter, Depends, HTTPException
from services.customer_service import CustomerService
from models.customer import Customer
from routes.auth import get_current_admin 

router = APIRouter()

@router.get("/", response_model=list[Customer])
async def get_customers(user=Depends(get_current_admin)):
    return CustomerService.get_all_customers()

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, user=Depends(get_current_admin)):
    try:
        return CustomerService.get_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{customer_id}")
async def update_customer(customer_id: int, name: str | None = None, email: str | None = None, 
                         phone_number: str | None = None, user=Depends(get_current_admin)):
    try:
        CustomerService.update_customer(customer_id, name, email, phone_number, user["user_id"])
        return {"message": "Customer updated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{customer_id}")
async def delete_customer(customer_id: int, user=Depends(get_current_admin)):
    try:
        CustomerService.delete_customer(customer_id, user["user_id"])
        return {"message": "Customer deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))