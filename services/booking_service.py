from database.connection import get_db
from models.ticket import Ticket
from repositories.booking_repository import BookingRepository
from repositories.seat_repository import SeatRepository
from repositories.ticket_repository import TicketRepository
from models.booking import BookingRequest, Booking

class BookingService:
    @staticmethod
    def get_all_bookings() -> list[Booking]:
        with get_db() as conn:
            repo = BookingRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_booking(booking_id: int) -> Booking:
        with get_db() as conn:
            repo = BookingRepository(conn)
            booking = repo.get_by_id(booking_id)
            if not booking:
                raise ValueError("Booking not found")
            return booking
        
    @staticmethod
    def get_bookings_by_customer(customer_id: int) -> list[Booking]:
        with get_db() as conn:
            repo = BookingRepository(conn)
            return repo.get_by_customer_id(customer_id)

    @staticmethod
    def book_tickets(booking: BookingRequest, customer_id: int) -> Booking:
        with get_db() as conn:
            booking_repo = BookingRepository(conn)
            seat_repo = SeatRepository(conn)
            ticket_repo = TicketRepository(conn)
            try:
                for seat_id in booking.seat_ids:
                    seat = seat_repo.get_by_id(seat_id)
                    if seat.status != "AVAILABLE":
                        raise ValueError(f"Seat {seat_id} is not available")
                    
                total_amount = sum(seat_repo.get_by_id(seat_id).price for seat_id in booking.seat_ids)
                
                booking_id = booking_repo.create(BookingRequest(
                    customer_id=customer_id,
                    total_amount=total_amount,
                    payment_method=booking.payment_method,
                    booking_status="PENDING"
                ))
                
                for seat_id in booking.seat_ids:
                    ticket_repo.create(Ticket(show_id=booking.show_id, booking_id=booking_id, seat_id=seat_id, ticket_type=booking.ticket_type))
                    seat_repo.update(seat_id, "BOOKED")
                
                booking_repo.update(booking_id, "CONFIRMED")
                conn.commit()
                return booking_id
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def update_booking(booking_id: int, total_amount: float | None, payment_method: str | None, 
                       status: str | None, admin_id: int) -> bool:
        with get_db() as conn:
            repo = BookingRepository(conn)
            if not repo.update(booking_id, total_amount, payment_method, status):
                raise ValueError("Booking not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "BOOKING", booking_id, "Updated booking details")
            return True

    @staticmethod
    def delete_booking(booking_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = BookingRepository(conn)
            if not repo.delete(booking_id):
                raise ValueError("Booking not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "BOOKING", booking_id, "Deleted booking")
            return True