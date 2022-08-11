from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.models import PostDB, OID
from pydantic import BaseModel, EmailStr
from app.auth.utils import signJWT, verify_token
from .schema import UserSchema
from app.config import get_config

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSchema, db: DatabaseManager = Depends(get_database)):
    res = await db.add_user(user.email, user.password)
    if res:
        return JSONResponse(status_code=201, content={"message": "User created"})
    return JSONResponse(status_code=409, content={"message": "User already exists"})


@router.get("/login")
async def login(
    email: EmailStr, password: str, db: DatabaseManager = Depends(get_database)
):
    id = await db.get_user(email, password)
    if id:
        token = signJWT(id)
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(
        status_code=401,
        content={"message": "Invalid credentials or user does not exist"},
    )


@router.get("/remove_user")
async def remove_user(
    email: str, admin_secret_key: str, db: DatabaseManager = Depends(get_database)
):
    if admin_secret_key == get_config().admin_secret_key:
        res = await db.remove_user(email)
        if res:
            return JSONResponse(status_code=200, content={"message": "User removed"})
        return JSONResponse(status_code=200, content={"message": "User does not exist"})
    return JSONResponse(status_code=401, content={"message": "Invalid credentials"})


@router.get("/verify_token/")
async def token_verify(token: str):
    res = verify_token(token)
    if res:
        return JSONResponse(status_code=200, content={"message": "Token verified"})
    return JSONResponse(
        status_code=401, content={"message": "Invalid or expired token"}
    )


@router.get("/refresh_token/")
async def refresh_token(token: str):
    res = verify_token(token)
    if res:
        token = signJWT(res)
        return JSONResponse(status_code=200, content={"token": token})
    return JSONResponse(
        status_code=401, content={"message": "Invalid or expired token"}
    )
