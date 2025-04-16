from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services.auth_service import AuthService
from services.customer_service import CustomerService
from models.customer import CustomerRegister
from models.admin import AdminCreate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/currentUser")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return AuthService.decode_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

async def get_current_admin(user: dict = Depends(get_current_user)):
    if user["user_type"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = AuthService.create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer", "user_type": user["user_type"]}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(customer: CustomerRegister):
    try:
        customer_id = CustomerService.register_customer(customer)
        return {"message": "Customer registered", "customer_id": customer_id}
    except Exception:
        raise HTTPException(status_code=400, detail="Registration failed")

@router.post("/register_admin", status_code=status.HTTP_201_CREATED)
async def register_admin(admin: AdminCreate, user=Depends(get_current_admin)):
    from database.connection import get_db
    from repositories.admin_repository import AdminRepository
    from repositories.login_repository import LoginRepository
    from utils.hashing import hash_password
    with get_db() as conn:
        admin_repo = AdminRepository(conn)
        login_repo = LoginRepository(conn)
        try:
            admin_id = admin_repo.create(admin)
            login_repo.create(admin.username, hash_password(admin.password), "ADMIN", admin_id)
            admin_repo.commit()
            from services.audit_service import AuditService
            AuditService.log_action(user["user_id"], "ADD", "ADMIN", admin_id, f"Added admin: {admin.name}")
            return {"message": "Admin registered", "admin_id": admin_id}
        except Exception:
            admin_repo.rollback()
            raise HTTPException(status_code=400, detail="Admin registration failed")
