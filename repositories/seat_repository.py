from repositories.base_repository import BaseRepository
from models.seat import Seat, SeatCreate, SeatUpdate

class SeatRepository(BaseRepository):
    def get_all(self) -> list[Seat]:
        self.cursor.execute("SELECT * FROM SEAT")
        return [Seat.from_orm(row) for row in self.cursor.fetchall()]

    def get_by_id(self, seat_id: int) -> Seat | None:
        self.cursor.execute("SELECT * FROM SEAT WHERE seat_id = ?", (seat_id,))
        row = self.cursor.fetchone()
        return Seat.from_orm(row) if row else None
    
    def get_by_layout_id(self, layout_id: int) -> list[Seat]:
        self.cursor.execute("SELECT * FROM SEAT WHERE layout_id = ?", (layout_id,))
        rows = self.cursor.fetchall()
        return [Seat.model_validate(dict(row)) for row in rows]

    def get_available_by_show(self, show_id: int) -> list[Seat]:
        self.cursor.execute(
            "SELECT s.* FROM SEAT s "
            "JOIN SEAT_LAYOUT sl ON s.layout_id = sl.layout_id "
            "JOIN SCREEN sc ON sl.screen_id = sc.screen_id "
            "JOIN SHOW sh ON sh.screen_id = sc.screen_id "
            "WHERE sh.show_id = ? AND s.status = 'AVAILABLE'", (show_id,)
        )
        return [Seat.from_orm(row) for row in self.cursor.fetchall()]

    def create(self, seat: SeatCreate) -> int:
        self.cursor.execute(
            "INSERT INTO SEAT (layout_id, row_label, seat_number, seat_category, is_accessible, price, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (seat.layout_id, seat.row_label, seat.seat_number, seat.seat_category, seat.is_accessible, seat.price, seat.status)
        )
        return self.cursor.lastrowid

    def update(self, seat_id: int, update: SeatUpdate) -> bool:
        updates = {k: v for k, v in update.dict().items() if v is not None}
        if not updates:
            return False
        query = "UPDATE SEAT SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE seat_id = ?"
        self.cursor.execute(query, list(updates.values()) + [seat_id])
        return self.cursor.rowcount > 0

    def delete(self, seat_id: int) -> bool:
        self.cursor.execute("DELETE FROM SEAT WHERE seat_id = ?", (seat_id,))
        return self.cursor.rowcount > 0