from repositories.base_repository import BaseRepository
from models.booking import Booking

class BookingRepository(BaseRepository):
    def get_all(self) -> list[Booking]:
        self.cursor.execute("SELECT * FROM BOOKING")
        return [Booking.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, booking_id: int) -> Booking | None:
        self.cursor.execute("SELECT * FROM BOOKING WHERE booking_id = ?", (booking_id,))
        row = self.cursor.fetchone()
        if row:
            return Booking.model_validate(dict(row))
        return None

    def create(self, customer_id: int, total_amount: float, payment_method: str, status: str) -> int:
        self.cursor.execute(
            "INSERT INTO BOOKING (customer_id, total_amount, payment_method, booking_status) VALUES (?, ?, ?, ?)",
            (customer_id, total_amount, payment_method, status)
        )
        return self.cursor.lastrowid
    
    def get_by_customer_id(self, customer_id: int) -> list[Booking]:
        self.cursor.execute("SELECT * FROM BOOKING WHERE customer_id = ?", (customer_id,))
        rows = self.cursor.fetchall()
        return [Booking.model_validate(dict(row)) for row in rows]

    def update(self, booking_id: int, total_amount: float | None = None, payment_method: str | None = None, 
               status: str | None = None) -> bool:
        updates = {k: v for k, v in {"total_amount": total_amount, "payment_method": payment_method, 
                                     "booking_status": status}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE BOOKING SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE booking_id = ?"
        self.cursor.execute(query, list(updates.values()) + [booking_id])
        return self.cursor.rowcount > 0

    def delete(self, booking_id: int) -> bool:
        self.cursor.execute("DELETE FROM BOOKING WHERE booking_id = ?", (booking_id,))
        return self.cursor.rowcount > 0