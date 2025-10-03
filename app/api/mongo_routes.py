from typing import List

from fastapi import APIRouter, Depends
from app.repositories.dependencies import get_mongo_repo
from app.repositories.mongo_repo import MongoMovieRepository

router = APIRouter()

@router.get("/movies")
async def list_movies(repo: MongoMovieRepository = Depends(get_mongo_repo)):
    return await repo.list_movies()
