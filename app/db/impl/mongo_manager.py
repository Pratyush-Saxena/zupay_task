import logging
from typing import Optional, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.db import DatabaseManager
from app.db.models import PostDB, OID
from app.rest.schema import PostSchema

class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = AsyncIOMotorClient(
            path
        )
        try:
            print(await self.client.server_info())
            self.db=self.client.main
            logging.info("Connected to MongoDB.")
            return True
        except Exception as e:
            print(e)
            print("ERROR: Unable to connect to the server.!!!")

    async def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")

    async def get_posts(self,user) -> List[PostSchema]:
        posts=await self.db.posts.find({'user':ObjectId(user)}).to_list(length=None)
        all_posts=[]
        for post in posts:
            post['id']=str(post['_id'])
            all_posts.append(PostSchema(**post).dict())
        return all_posts


    async def delete_post(self, post_id: OID,user:str):
        res=await self.db.posts.find_one({'_id': ObjectId(post_id),'user':ObjectId(user)})
        if res:
            await self.db.posts.delete_one({'_id': ObjectId(post_id),'user':ObjectId(user)})
            return True
        return False


    async def update_post(self, post: PostSchema,user:str):
        post_id=ObjectId(post.id)
        res=await self.db.posts.find_one({'_id': ObjectId(post_id),'user':ObjectId(user)})
        if res:
            await self.db.posts.update_one({'_id': ObjectId(post_id),'user':ObjectId(user)},{'$set':post.dict(exclude={'id'})})
            return True
        return False

    async def add_post(self, post: PostSchema,user:str):
        await self.db.posts.insert_one({**post.dict(exclude={'id'}),'user':ObjectId(user)})
        
    
    async def add_user(self, email: str, password: str):
        resp = await self.db.users.find_one({'email': email})
        if resp:
            return False
        await self.db.users.insert_one({'email': email, 'password': password})
        return True
    
    async def get_user(self, email: str, password: str) -> Optional[OID]:
        user = await self.db.users.find_one({'email': email, 'password': password})
        if user:
            return str(user['_id'])
    
    async def remove_user(self, email: str):
        if await self.db.users.find_one({'email': email}):
            await self.db.users.delete_one({'email': email})
            return True
        return False