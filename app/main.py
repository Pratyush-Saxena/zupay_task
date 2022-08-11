import uvicorn
from fastapi import FastAPI,Request,Depends

from pydantic import BaseModel
from app.config import get_config
from app.db import db
from app.rest import posts,auth
from typing import Union
import os

app = FastAPI(title="ToDo App", docs_url="/api/v1/docs", redoc_url="/api/v1/redoc")

app.include_router(posts.router, prefix='/todo',)
app.include_router(auth.router, prefix='/auth',)




@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path)



@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
