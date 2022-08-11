from abc import abstractmethod
from typing import List, Optional
from pydantic import EmailStr
from app.db.models import OID, UserDB
from app.rest.schema import PostSchema
class DatabaseManager(object):
    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def get_posts(self) -> List[PostSchema]:
        pass


    @abstractmethod
    async def add_post(self, post: PostSchema):
        pass

    @abstractmethod
    async def update_post(self, post: PostSchema):
        pass

    @abstractmethod
    async def delete_post(self, post_id: OID):
        pass

    @abstractmethod
    async def add_user(self, email: EmailStr, password: str):
        pass

    @abstractmethod
    async def get_user(self, email: EmailStr, password: str) -> Optional[OID]:
        pass

    @abstractmethod
    async def remove_user(self, email: str):
        pass


