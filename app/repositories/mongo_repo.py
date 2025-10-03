from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from app.config             import settings

class MongoMovieRepository:
    def __init__(self, uri: str = None, db_name: str = None):
        # fallback to config if no args passed
        self.client = AsyncIOMotorClient(uri or settings.MONGO_URI)
        self.db     = self.client[db_name or settings.MONGO_DB]
        self.collection = self.db["movies"]

    async def list_movies(self) -> List[dict]:
        docs = await self.collection.find().to_list(length=1000)
        transformed: List[dict] = []
        for doc in docs:
            doc["id"] = str(doc.pop("_id"))   # move and cast ObjectId/string
            transformed.append(doc)
        return transformed

