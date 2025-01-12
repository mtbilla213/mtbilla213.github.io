import logging
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users = self.db.users

    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        try:
            existing_user = await self.get_user(user_id)
            if not existing_user:
                logging.info(f"Adding new user: {user_id}")
                await self.users.insert_one({
                    "user_id": user_id,
                    "username": username,
                    "first_name": first_name,
                    "points": 0,
                    "streak": 0
                })
                return True
            logging.info(f"User already exists: {user_id}")
            return False
        except Exception as e:
            logging.error(f"Error adding user to database: {e}")
            return False

    async def get_user(self, user_id: int):
        try:
            return await self.users.find_one({"user_id": user_id})
        except Exception as e:
            logging.error(f"Error getting user from database: {e}")
            return None