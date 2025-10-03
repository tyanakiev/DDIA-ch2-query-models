from fastapi import APIRouter, Depends
from app.models.domain import Movie
from app.repositories.dependencies import get_neo4j_repo

router = APIRouter()

@router.get("/movies", response_model=list[Movie])
async def list_movies(repo = Depends(get_neo4j_repo)):
    return await repo.list_movies()