from database.connection import get_db
from repositories.show_repository import ShowRepository
from models.show import Show, ShowCreate, ShowUpdate
from services.audit_service import AuditService

class ShowService:
    @staticmethod
    def get_all_shows() -> list[Show]:
        with get_db() as conn:
            repo = ShowRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_show(show_id: int) -> Show:
        with get_db() as conn:
            repo = ShowRepository(conn)
            show = repo.get_by_id(show_id)
            if not show:
                raise ValueError("Show not found")
            return show

    @staticmethod
    def get_shows_by_movie(movie_id: int) -> list[Show]:
        with get_db() as conn:
            repo = ShowRepository(conn)
            return repo.get_by_movie(movie_id)
        
    @staticmethod
    def get_shows_by_screen(screen_id: int) -> list[Show]:
        with get_db() as conn:
            repo = ShowRepository(conn)
            return repo.get_by_screen_id(screen_id)

    @staticmethod
    def create_show(show: ShowCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = ShowRepository(conn)
            show_id = repo.create(show)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "SHOW", show_id, f"Added show at {show.show_time}")
            return show_id

    @staticmethod
    def update_show(show_id: int, update: ShowUpdate, admin_id: int) -> bool:
        with get_db() as conn:
            repo = ShowRepository(conn)
            if not repo.update(show_id, update):
                raise ValueError("Show not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "SHOW", show_id, "Updated show details")
            return True

    @staticmethod
    def delete_show(show_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = ShowRepository(conn)
            if not repo.delete(show_id):
                raise ValueError("Show not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "SHOW", show_id, "Deleted show")
            return True