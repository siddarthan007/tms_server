from database.connection import get_db
from repositories.admin_repository import AdminRepository
from repositories.login_repository import LoginRepository
from models.admin import Admin, AdminCreate
from utils.hashing import hash_password
from services.audit_service import AuditService

class AdminService:
    @staticmethod
    def get_all_admins() -> list[Admin]:
        with get_db() as conn:
            repo = AdminRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_admin(admin_id: int) -> Admin:
        with get_db() as conn:
            repo = AdminRepository(conn)
            admin = repo.get_by_id(admin_id)
            if not admin:
                raise ValueError("Admin not found")
            return admin

    @staticmethod
    def create_admin(admin: AdminCreate, creator_admin_id: int) -> int:
        with get_db() as conn:
            admin_repo = AdminRepository(conn)
            login_repo = LoginRepository(conn)
            try:
                admin_id = admin_repo.create(admin)
                # Validate user_id exists in ADMIN table
                if not admin_repo.get_by_id(admin_id):
                    raise ValueError("Invalid admin_id")
                login_repo.create(admin.username, hash_password(admin.password), "ADMIN", admin_id)
                admin_repo.commit()
                AuditService.log_action(creator_admin_id, "ADD", "ADMIN", admin_id, f"Added admin: {admin.name}")
                return admin_id
            except Exception as e:
                admin_repo.rollback()
                raise e

    @staticmethod
    def update_admin(admin_id: int, name: str | None, email: str | None, phone_number: str | None, 
                     role: str | None, updater_admin_id: int) -> bool:
        with get_db() as conn:
            repo = AdminRepository(conn)
            if not repo.update(admin_id, name, email, phone_number, role):
                raise ValueError("Admin not found or no changes")
            repo.commit()
            AuditService.log_action(updater_admin_id, "UPDATE", "ADMIN", admin_id, "Updated admin details")
            return True

    @staticmethod
    def delete_admin(admin_id: int, deleter_admin_id: int) -> bool:
        with get_db() as conn:
            repo = AdminRepository(conn)
            if not repo.delete(admin_id):
                raise ValueError("Admin not found")
            repo.commit()
            AuditService.log_action(deleter_admin_id, "DELETE", "ADMIN", admin_id, "Deleted admin")
            return True