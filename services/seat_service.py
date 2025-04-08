from database.connection import get_db
from repositories.seat_repository import SeatRepository
from models.seat import Seat, SeatCreate, SeatUpdate
from services.audit_service import AuditService

class SeatService:
    @staticmethod
    def get_all_seats() -> list[Seat]:
        with get_db() as conn:
            repo = SeatRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_seat(seat_id: int) -> Seat:
        with get_db() as conn:
            repo = SeatRepository(conn)
            seat = repo.get_by_id(seat_id)
            if not seat:
                raise ValueError("Seat not found")
            return seat

    @staticmethod
    def get_available_seats(show_id: int) -> list[Seat]:
        with get_db() as conn:
            repo = SeatRepository(conn)
            return repo.get_available_by_show(show_id)
        
    @staticmethod
    def get_seats_by_layout(layout_id: int) -> list[Seat]:
        with get_db() as conn:
            repo = SeatRepository(conn)
            return repo.get_by_layout_id(layout_id)

    @staticmethod
    def create_seat(seat: SeatCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = SeatRepository(conn)
            seat_id = repo.create(seat)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "SEAT", seat_id, f"Added seat: {seat.row_label}{seat.seat_number}")
            return seat_id

    @staticmethod
    def update_seat(seat_id: int, update: SeatUpdate, admin_id: int) -> bool:
        with get_db() as conn:
            repo = SeatRepository(conn)
            if not repo.update(seat_id, update):
                raise ValueError("Seat not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "SEAT", seat_id, "Updated seat details")
            return True

    @staticmethod
    def delete_seat(seat_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = SeatRepository(conn)
            if not repo.delete(seat_id):
                raise ValueError("Seat not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "SEAT", seat_id, "Deleted seat")
            return True