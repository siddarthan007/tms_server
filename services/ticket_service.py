from database.connection import get_db
from repositories.ticket_repository import TicketRepository
from models.ticket import Ticket, TicketCreate, TicketUpdate
from services.audit_service import AuditService

class TicketService:
    @staticmethod
    def get_all_tickets() -> list[Ticket]:
        with get_db() as conn:
            repo = TicketRepository(conn)
            return repo.get_all()

    @staticmethod
    def get_ticket(ticket_id: int) -> Ticket:
        with get_db() as conn:
            repo = TicketRepository(conn)
            ticket = repo.get_by_id(ticket_id)
            if not ticket:
                raise ValueError("Ticket not found")
            return ticket
        
    @staticmethod
    def get_tickets_by_booking(booking_id: int) -> list[Ticket]:
        with get_db() as conn:
            repo = TicketRepository(conn)
            return repo.get_by_booking_id(booking_id)
        
    @staticmethod
    def get_tickets_by_show(show_id: int) -> list[Ticket]:
        with get_db() as conn:
            repo = TicketRepository(conn)
            return repo.get_by_show_id(show_id)

    @staticmethod
    def create_ticket(ticket: TicketCreate, admin_id: int) -> int:
        with get_db() as conn:
            repo = TicketRepository(conn)
            ticket_id = repo.create(ticket)
            repo.commit()
            AuditService.log_action(admin_id, "ADD", "TICKET", ticket_id, f"Added ticket for show {ticket.show_id}")
            return ticket_id

    @staticmethod
    def update_ticket(ticket_id: int, update: TicketUpdate, admin_id: int) -> bool:
        with get_db() as conn:
            repo = TicketRepository(conn)
            if not repo.update(ticket_id, update):
                raise ValueError("Ticket not found or no changes")
            repo.commit()
            AuditService.log_action(admin_id, "UPDATE", "TICKET", ticket_id, "Updated ticket details")
            return True

    @staticmethod
    def delete_ticket(ticket_id: int, admin_id: int) -> bool:
        with get_db() as conn:
            repo = TicketRepository(conn)
            if not repo.delete(ticket_id):
                raise ValueError("Ticket not found")
            repo.commit()
            AuditService.log_action(admin_id, "DELETE", "TICKET", ticket_id, "Deleted ticket")
            return True