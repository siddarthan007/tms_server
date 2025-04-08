from database.connection import get_db
from repositories.screen_repository import ScreenRepository
from models.screen import Screen, ScreenCreate

class ScreenService:
    @staticmethod
    def get_all_screens() -> list[Screen]:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_screen(screen_id: int) -> Screen:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            screen = repo.get_by_id(screen_id)
            if not screen:
                raise ValueError("Screen not found")
            return screen
        
    @staticmethod
    def get_screens_by_theatre(theatre_id: int) -> list[Screen]:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            return repo.get_by_theatre_id(theatre_id)

    @staticmethod
    def add_screen(screen: ScreenCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            screen_id = repo.create(screen)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "SCREEN", screen_id, f"Added screen: {screen.screen_name}")
            return screen_id

    @staticmethod
    def update_screen(screen_id: int, theatre_id: int | None, screen_name: str | None, 
                      capacity: int | None, admin_id: int) -> bool:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            if not repo.update(screen_id, theatre_id, screen_name, capacity):
                raise ValueError("Screen not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "SCREEN", screen_id, "Updated screen details")
            return True

    @staticmethod
    def delete_screen(screen_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = ScreenRepository(conn)
            if not repo.delete(screen_id):
                raise ValueError("Screen not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "SCREEN", screen_id, "Deleted screen")
            return True