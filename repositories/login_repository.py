from repositories.base_repository import BaseRepository
from models.login import Login
from datetime import datetime

class LoginRepository(BaseRepository):
    def create(self, username: str, password_hash: str, user_type: str, user_id: int) -> int:
        self.cursor.execute(
            "INSERT INTO LOGIN (username, password_hash, user_type, user_id) VALUES (?, ?, ?, ?)",
            (username, password_hash, user_type, user_id)
        )
        return self.cursor.lastrowid

    def get_by_username(self, username: str) -> Login | None:
        self.cursor.execute("SELECT * FROM LOGIN WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            row_dict = dict(row)
            return Login.model_validate(row_dict)
        return None

    def update_last_login(self, login_id: int):
        self.cursor.execute(
            "UPDATE LOGIN SET last_login = ? WHERE login_id = ?",
            (datetime.now().isoformat(), login_id)
        )