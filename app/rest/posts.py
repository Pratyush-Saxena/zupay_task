from app.auth.utils import verify_token, get_user_id
from app.config import get_config
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db import DatabaseManager, get_database
from app.db.models import PostDB, OID
from app.auth import oauth2
from .schema import PostSchema

router = APIRouter()


@router.get("/")
async def all_posts(
    db: DatabaseManager = Depends(get_database), token: str = Depends(oauth2)
):
    if not (token and verify_token(token)):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    user = get_user_id(token)
    posts = await db.get_posts(user=user)
    return JSONResponse(status_code=200, content={"posts": posts})


@router.put("/")
async def update_post(
    post: PostSchema,
    db: DatabaseManager = Depends(get_database),
    token: str = Depends(oauth2),
):
    if not (token and verify_token(token)):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    user = get_user_id(token)
    resp = await db.update_post(post=post, user=user)
    if resp:
        return JSONResponse(status_code=200, content={"message": "Post updated"})
    return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/", status_code=201)
async def add_post(
    post_response: PostSchema,
    db: DatabaseManager = Depends(get_database),
    token: str = Depends(oauth2),
):
    if not (token and verify_token(token)):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    user = get_user_id(token)
    await db.add_post(post_response, user)
    return JSONResponse(status_code=201, content={"message": "Post created"})


@router.delete("/")
async def delete_post(
    post_id: OID,
    db: DatabaseManager = Depends(get_database),
    token: str = Depends(oauth2),
):
    if not (token and verify_token(token)):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    user = get_user_id(token)
    resp = await db.delete_post(post_id=post_id, user=user)
    if resp:
        return JSONResponse(status_code=200, content={"message": "Post deleted"})
    return JSONResponse(status_code=404, content={"message": "Post not found"})
