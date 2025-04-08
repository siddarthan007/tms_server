from repositories.base_repository import BaseRepository
from models.admin import Admin, AdminCreate

class AdminRepository(BaseRepository):
    def get_all(self) -> list[Admin]:
        self.cursor.execute("SELECT * FROM ADMIN")
        return [Admin.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, admin_id: int) -> Admin | None:
        self.cursor.execute("SELECT * FROM ADMIN WHERE admin_id = ?", (admin_id,))
        row = self.cursor.fetchone()
        return Admin.model_validate(dict(row)) if row else None

    def create(self, admin: AdminCreate) -> int:
        self.cursor.execute(
            "INSERT INTO ADMIN (name, email, phone_number, role) VALUES (?, ?, ?, ?)",
            (admin.name, admin.email, admin.phone_number, admin.role)
        )
        return self.cursor.lastrowid

    def update(self, admin_id: int, name: str | None = None, email: str | None = None, 
               phone_number: str | None = None, role: str | None = None) -> bool:
        updates = {k: v for k, v in {"name": name, "email": email, "phone_number": phone_number, "role": role}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE ADMIN SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE admin_id = ?"
        self.cursor.execute(query, list(updates.values()) + [admin_id])
        return self.cursor.rowcount > 0

    def delete(self, admin_id: int) -> bool:
        self.cursor.execute("DELETE FROM ADMIN WHERE admin_id = ?", (admin_id,))
        return self.cursor.rowcount > 0