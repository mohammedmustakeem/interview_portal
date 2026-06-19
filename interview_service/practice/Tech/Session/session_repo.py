from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class SessionRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["interview_sessions"]

    async def create(self, session_data: dict):
        await self.collection.insert_one(session_data)

    async def get(self, session_id: str):
        return await self.collection.find_one(
            {"session_id": session_id}
        )

    async def update(self, session_id: str, update_fields: dict):
        update_fields["updated_at"] = datetime.utcnow()

        await self.collection.update_one(
            {"session_id": session_id},
            {"$set": update_fields}
        )

    async def push_to_array(self, session_id: str, field: str, value):
        await self.collection.update_one(
            {"session_id": session_id},
            {"$push": {field: value}}
        )
