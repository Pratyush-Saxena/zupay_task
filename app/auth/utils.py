from logging import exception
import time
from typing import Dict

import jwt
from app.config import get_config


JWT_SECRET = get_config().jwt_secret
JWT_ALGORITHM = get_config().hash_algorithm


def signJWT(user_id: str) -> Dict[str, str]:
    try:
        payload = {"user_id": user_id, "expires": time.time() + 1800}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"token": token}
    except Exception as e:
        print(e)
        return {"message": "Something went wrong"}


def verify_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        print(e)
        return None


def refresh_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return signJWT(decoded_token["user_id"])
    except Exception as e:
        print(e)
        return None


def get_user_id(token: str) -> str:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token["user_id"]
    except Exception as e:
        print(e)
        return None
