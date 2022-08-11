from app.db.models import OID
from pydantic import BaseModel
from typing import Optional

class PostSchema(BaseModel):
    id : Optional[OID]
    title: str
    description: str

class UserSchema(BaseModel):
    email: str
    password: str