from database.connection import get_db
from repositories.customer_repository import CustomerRepository
from repositories.login_repository import LoginRepository
from models.customer import CustomerRegister, Customer
from utils.hashing import hash_password

class CustomerService:
    @staticmethod
    def get_all_customers() -> list[Customer]:
        with get_db() as conn:
            repo = CustomerRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_customer(customer_id: int) -> Customer:
        with get_db() as conn:
            repo = CustomerRepository(conn)
            customer = repo.get_by_id(customer_id)
            if not customer:
                raise ValueError("Customer not found")
            return customer

    @staticmethod
    def register_customer(customer: CustomerRegister) -> int:
        with get_db() as conn:
            customer_repo = CustomerRepository(conn)
            login_repo = LoginRepository(conn)
            try:
                customer_id = customer_repo.create(customer)
                if not customer_repo.get_by_id(customer_id):
                    raise ValueError("Invalid customer_id")
                login_repo.create(customer.username, hash_password(customer.password), "CUSTOMER", customer_id)
                customer_repo.commit()
                return customer_id
            except Exception as e:
                customer_repo.rollback()
                raise e

    @staticmethod
    def update_customer(customer_id: int, name: str | None, email: str | None, phone_number: str | None, 
                        admin_id: int) -> bool:
        with get_db() as conn:
            repo = CustomerRepository(conn)
            if not repo.update(customer_id, name, email, phone_number):
                raise ValueError("Customer not found or no changes")
            repo.commit()
            from services.audit_service import AuditService
            AuditService.log_action(admin_id, "UPDATE", "CUSTOMER", customer_id, "Updated customer details")
            return True

    @staticmethod
    def delete_customer(customer_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = CustomerRepository(conn)
            if not repo.delete(customer_id):
                raise ValueError("Customer not found")
            repo.commit()
            from services.audit_service import AuditService
            AuditService.log_action(admin_id, "DELETE", "CUSTOMER", customer_id, "Deleted customer")
            return True