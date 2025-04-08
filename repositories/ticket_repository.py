from repositories.base_repository import BaseRepository
from models.ticket import Ticket, TicketCreate, TicketUpdate

class TicketRepository(BaseRepository):
    def get_all(self) -> list[Ticket]:
        self.cursor.execute("SELECT * FROM TICKET")
        return [Ticket.from_orm(row) for row in self.cursor.fetchall()]

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        self.cursor.execute("SELECT * FROM TICKET WHERE ticket_id = ?", (ticket_id,))
        row = self.cursor.fetchone()
        if row:
            return Ticket.model_validate(dict(row))
        return None

    def create(self, ticket: TicketCreate) -> int:
        self.cursor.execute(
            "INSERT INTO TICKET (show_id, booking_id, seat_id, ticket_type) VALUES (?, ?, ?, ?)",
            (ticket.show_id, ticket.booking_id, ticket.seat_id, ticket.ticket_type)
        )
        return self.cursor.lastrowid
    
    def get_by_booking_id(self, booking_id: int) -> list[Ticket]:
        self.cursor.execute("SELECT * FROM TICKET WHERE booking_id = ?", (booking_id,))
        rows = self.cursor.fetchall()
        return [Ticket.model_validate(dict(row)) for row in rows]

    def get_by_show_id(self, show_id: int) -> list[Ticket]:
        self.cursor.execute("SELECT * FROM TICKET WHERE show_id = ?", (show_id,))
        rows = self.cursor.fetchall()
        return [Ticket.model_validate(dict(row)) for row in rows]

    def update(self, ticket_id: int, update: TicketUpdate) -> bool:
        updates = {k: v for k, v in update.dict().items() if v is not None}
        if not updates:
            return False
        query = "UPDATE TICKET SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE ticket_id = ?"
        self.cursor.execute(query, list(updates.values()) + [ticket_id])
        return self.cursor.rowcount > 0

    def delete(self, ticket_id: int) -> bool:
        self.cursor.execute("DELETE FROM TICKET WHERE ticket_id = ?", (ticket_id,))
        return self.cursor.rowcount > 0