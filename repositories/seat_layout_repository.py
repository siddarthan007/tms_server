from repositories.base_repository import BaseRepository
from models.seat_layout import SeatLayout, SeatLayoutUpdate, SeatLayoutCreate

class SeatLayoutRepository(BaseRepository):
    def get_by_id(self, layout_id: int) -> SeatLayout | None:
        self.cursor.execute("SELECT * FROM SEAT_LAYOUT WHERE layout_id = ?", (layout_id,))
        row = self.cursor.fetchone()
        return SeatLayout.model_validate(dict(row)) if row else None
    
    def get_all(self) -> list[SeatLayout]:
        self.cursor.execute("SELECT * FROM SEAT_LAYOUT")
        rows = self.cursor.fetchall()
        return [SeatLayout.model_validate(dict(row)) for row in rows]

    def get_by_screen_id(self, screen_id: int) -> list[SeatLayout]:
        self.cursor.execute("SELECT * FROM SEAT_LAYOUT WHERE screen_id = ?", (screen_id,))
        rows = self.cursor.fetchall()
        return [SeatLayout.model_validate(dict(row)) for row in rows]
    
    def create(self, seat_layout: SeatLayoutCreate) -> int:
        self.cursor.execute(
            "INSERT INTO SEAT_LAYOUT (screen_id, layout_name, layout_type, total_rows, total_columns) "
            "VALUES (?, ?, ?, ?, ?)",
            (seat_layout.screen_id, seat_layout.layout_name, seat_layout.layout_type, 
             seat_layout.total_rows, seat_layout.total_columns)
        )
        return self.cursor.lastrowid

    def update(self, layout_id: int, update: SeatLayoutUpdate) -> bool:
        updates = {k: v for k, v in update.dict().items() if v is not None}
        if not updates:
            return False
        query = "UPDATE SEAT_LAYOUT SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE layout_id = ?"
        self.cursor.execute(query, list(updates.values()) + [layout_id])
        return self.cursor.rowcount > 0

    def delete(self, layout_id: int) -> bool:
        self.cursor.execute("DELETE FROM SEAT_LAYOUT WHERE layout_id = ?", (layout_id,))
        return self.cursor.rowcount > 0