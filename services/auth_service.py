from datetime import datetime, timedelta, timezone
from jose import jwt
from config import Config
from database.connection import get_db
from repositories.login_repository import LoginRepository
from utils.hashing import hash_password, verify_password

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict | None:
        with get_db() as conn:
            repo = LoginRepository(conn)
            login = repo.get_by_username(username)
            if login and verify_password(password, login.password_hash):
                repo.update_last_login(login.login_id)
                repo.commit()
                return {"username": login.username, "user_type": login.user_type, "user_id": login.user_id}
        return None

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise ValueError("Invalid token")
        with get_db() as conn:
            repo = LoginRepository(conn)
            login = repo.get_by_username(username)
            if not login:
                raise ValueError("User not found")
            return {"username": login.username, "user_type": login.user_type, "user_id": login.user_id}