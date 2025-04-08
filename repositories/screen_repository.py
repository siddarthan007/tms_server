from repositories.base_repository import BaseRepository
from models.screen import Screen, ScreenCreate

class ScreenRepository(BaseRepository):
    def get_all(self) -> list[Screen]:
        self.cursor.execute("SELECT * FROM SCREEN")
        return [Screen.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, screen_id: int) -> Screen | None:
        self.cursor.execute("SELECT * FROM SCREEN WHERE screen_id = ?", (screen_id,))
        row = self.cursor.fetchone()
        return Screen.model_validate(dict(row)) if row else None

    def get_by_theatre_id(self, theatre_id: int) -> list[Screen]:
        self.cursor.execute("SELECT * FROM SCREEN WHERE theatre_id = ?", (theatre_id,))
        rows = self.cursor.fetchall()
        return [Screen.model_validate(dict(row)) for row in rows]

    def create(self, screen: ScreenCreate) -> int:
        self.cursor.execute(
            "INSERT INTO SCREEN (theatre_id, screen_name, capacity) VALUES (?, ?, ?)",
            (screen.theatre_id, screen.screen_name, screen.capacity)
        )
        return self.cursor.lastrowid

    def update(self, screen_id: int, theatre_id: int | None = None, screen_name: str | None = None, 
               capacity: int | None = None) -> bool:
        updates = {k: v for k, v in {"theatre_id": theatre_id, "screen_name": screen_name, "capacity": capacity}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE SCREEN SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE screen_id = ?"
        self.cursor.execute(query, list(updates.values()) + [screen_id])
        return self.cursor.rowcount > 0

    def delete(self, screen_id: int) -> bool:
        self.cursor.execute("DELETE FROM SCREEN WHERE screen_id = ?", (screen_id,))
        return self.cursor.rowcount > 0