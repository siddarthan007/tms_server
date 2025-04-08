from repositories.base_repository import BaseRepository
from models.customer import Customer, CustomerRegister

class CustomerRepository(BaseRepository):
    def get_all(self) -> list[Customer]:
        self.cursor.execute("SELECT * FROM CUSTOMER")
        return [Customer.model_validate(dict(row)) for row in self.cursor.fetchall()]

    def get_by_id(self, customer_id: int) -> Customer | None:
        self.cursor.execute("SELECT * FROM CUSTOMER WHERE customer_id = ?", (customer_id,))
        row = self.cursor.fetchone()
        if row:
            return Customer.model_validate(dict(row))
        return None

    def create(self, customer: CustomerRegister) -> int:
        self.cursor.execute(
            "INSERT INTO CUSTOMER (name, email, phone_number) VALUES (?, ?, ?)",
            (customer.name, customer.email, customer.phone_number)
        )
        return self.cursor.lastrowid

    def update(self, customer_id: int, name: str | None = None, email: str | None = None, 
               phone_number: str | None = None) -> bool:
        updates = {k: v for k, v in {"name": name, "email": email, "phone_number": phone_number}.items() if v is not None}
        if not updates:
            return False
        query = "UPDATE CUSTOMER SET " + ", ".join(f"{k} = ?" for k in updates) + " WHERE customer_id = ?"
        self.cursor.execute(query, list(updates.values()) + [customer_id])
        return self.cursor.rowcount > 0

    def delete(self, customer_id: int) -> bool:
        self.cursor.execute("DELETE FROM CUSTOMER WHERE customer_id = ?", (customer_id,))
        return self.cursor.rowcount > 0