from database.connection import get_db
from repositories.seat_layout_repository import SeatLayoutRepository
from models.seat_layout import SeatLayout, SeatLayoutCreate, SeatLayoutUpdate
from services.audit_service import AuditService

class SeatLayoutService:
    @staticmethod
    def get_seat_layout(layout_id: int) -> SeatLayout:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            layout = repo.get_by_id(layout_id)
            if not layout:
                raise ValueError("Seat layout not found")
            return layout
        
    @staticmethod
    def get_all_seat_layouts() -> list[SeatLayout]:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_seat_layouts_by_screen(screen_id: int) -> list[SeatLayout]:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            return repo.get_by_screen_id(screen_id)
        
    def create_seat_layout(seat_layout: SeatLayoutCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            try:
                layout_id = repo.create(seat_layout)
                conn.commit()
                AuditService.log_action(admin_id, "ADD", "SEAT_LAYOUT", layout_id, 
                                      f"Added seat layout for screen {seat_layout.screen_id}")
                return layout_id
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def update_seat_layout(layout_id: int, update: SeatLayoutUpdate, admin_id: int) -> bool:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            if not repo.update(layout_id, update):
                raise ValueError("Seat layout not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "SEAT_LAYOUT", layout_id, "Updated seat layout")
            return True

    @staticmethod
    def delete_seat_layout(layout_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = SeatLayoutRepository(conn)
            if not repo.delete(layout_id):
                raise ValueError("Seat layout not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "SEAT_LAYOUT", layout_id, "Deleted seat layout")
            return True