from database.connection import get_db
from repositories.theatre_repository import TheatreRepository
from models.theatre import Theatre

class TheatreService:
    @staticmethod
    def get_all_theatres() -> list[Theatre]:
        with get_db() as conn:
            repo = TheatreRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_theatre(theatre_id: int) -> Theatre:
        with get_db() as conn:
            repo = TheatreRepository(conn)
            theatre = repo.get_by_id(theatre_id)
            if not theatre:
                raise ValueError("Theatre not found")
            return theatre

    @staticmethod
    def create_theatre(name: str, location: str | None, contact_number: str | None, admin_id: int) -> int:
        with get_db() as conn:
            repo = TheatreRepository(conn)
            theatre_id = repo.create(name, location, contact_number)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "THEATRE", theatre_id, f"Added theatre: {name}")
            return theatre_id

    @staticmethod
    def update_theatre(theatre_id: int, name: str | None, location: str | None, 
                       contact_number: str | None, admin_id: int) -> bool:
        with get_db() as conn:
            repo = TheatreRepository(conn)
            if not repo.update(theatre_id, name, location, contact_number):
                raise ValueError("Theatre not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "THEATRE", theatre_id, "Updated theatre details")
            return True

    @staticmethod
    def delete_theatre(theatre_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = TheatreRepository(conn)
            if not repo.delete(theatre_id):
                raise ValueError("Theatre not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "THEATRE", theatre_id, "Deleted theatre")
            return True