from repositories.base_repository import BaseRepository
from models.show import Show, ShowCreate, ShowUpdate

class ShowRepository(BaseRepository):
    def get_all(self) -> list[Show]:
        self.cursor.execute(
            "SELECT s.*, t.name AS theatre_name, sc.screen_name FROM SHOW s "
            "JOIN SCREEN sc ON s.screen_id = sc.screen_id "
            "JOIN THEATRE t ON sc.theatre_id = t.theatre_id"
        )
        return [Show.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, show_id: int) -> Show | None:
        self.cursor.execute(
            "SELECT s.*, t.name AS theatre_name, sc.screen_name FROM SHOW s "
            "JOIN SCREEN sc ON s.screen_id = sc.screen_id "
            "JOIN THEATRE t ON sc.theatre_id = t.theatre_id "
            "WHERE s.show_id = ?", (show_id,)
        )
        row = self.cursor.fetchone()
        return Show.model_validate(dict(row)) if row else None

    def get_by_movie(self, movie_id: int) -> list[Show]:
        self.cursor.execute(
            "SELECT s.*, t.name AS theatre_name, sc.screen_name FROM SHOW s "
            "JOIN SCREEN sc ON s.screen_id = sc.screen_id "
            "JOIN THEATRE t ON sc.theatre_id = t.theatre_id "
            "WHERE s.movie_id = ? AND s.status = 'ACTIVE'", (movie_id,)
        )
        return [Show.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def create(self, show: ShowCreate) -> int:
        self.cursor.execute(
            "INSERT INTO SHOW (movie_id, screen_id, show_time, ticket_price, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (show.movie_id, show.screen_id, show.show_time, show.ticket_price, show.status)
        )
        return self.cursor.lastrowid
    
    def get_by_screen_id(self, screen_id: int) -> list[Show]:
        self.cursor.execute("SELECT * FROM SHOW WHERE screen_id = ?", (screen_id,))
        rows = self.cursor.fetchall()
        return [Show.model_validate(dict(row)) for row in rows]

    def update(self, show_id: int, update: ShowUpdate) -> bool:
        updates = {k: v for k, v in update.dict().items() if v is not None}
        if not updates:
            return False
        query = "UPDATE SHOW SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE show_id = ?"
        self.cursor.execute(query, list(updates.values()) + [show_id])
        return self.cursor.rowcount > 0

    def delete(self, show_id: int) -> bool:
        self.cursor.execute("DELETE FROM SHOW WHERE show_id = ?", (show_id,))
        return self.cursor.rowcount > 0