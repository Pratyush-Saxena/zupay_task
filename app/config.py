from functools import lru_cache
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    app_name: str = "ToDo App"
    db_path: str = os.getenv("DB_PATH")
    debug: bool = False
    hash_algorithm: str = os.getenv("HASH_ALGORITHM")
    jwt_secret: str = os.getenv("JWT_SECRET")
    admin_secret_key: str = os.getenv("SECRET_KEY")


@lru_cache()
def get_config():
    return Config()
