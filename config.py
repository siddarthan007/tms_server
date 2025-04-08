import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-jamesbond-007")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    DB_PATH = "theatre.db"