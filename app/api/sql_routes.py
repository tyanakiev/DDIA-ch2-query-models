from fastapi import APIRouter, Depends
from app.models.domain import Movie
from app.repositories.dependencies import get_sql_repo

router = APIRouter()

@router.get("/movies", response_model=list[Movie])
async def list_movies(repo = Depends(get_sql_repo)):
    return await repo.list_movies()