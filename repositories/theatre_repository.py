from repositories.base_repository import BaseRepository
from models.theatre import Theatre

class TheatreRepository(BaseRepository):
    def get_all(self) -> list[Theatre]:
        self.cursor.execute("SELECT * FROM THEATRE")
        return [Theatre.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, theatre_id: int) -> Theatre | None:
        self.cursor.execute("SELECT * FROM THEATRE WHERE theatre_id = ?", (theatre_id,))
        row = self.cursor.fetchone()
        if row:
            return Theatre.model_validate(dict(row))
        return None

    def create(self, name: str, location: str | None = None, contact_number: str | None = None) -> int:
        self.cursor.execute(
            "INSERT INTO THEATRE (name, location, contact_number) VALUES (?, ?, ?)",
            (name, location, contact_number)
        )
        return self.cursor.lastrowid

    def update(self, theatre_id: int, name: str | None = None, location: str | None = None, 
               contact_number: str | None = None) -> bool:
        updates = {k: v for k, v in {"name": name, "location": location, "contact_number": contact_number}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE THEATRE SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE theatre_id = ?"
        self.cursor.execute(query, list(updates.values()) + [theatre_id])
        return self.cursor.rowcount > 0

    def delete(self, theatre_id: int) -> bool:
        self.cursor.execute("DELETE FROM THEATRE WHERE theatre_id = ?", (theatre_id,))
        return self.cursor.rowcount > 0