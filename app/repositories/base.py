from abc import ABC, abstractmethod
from typing import List
from app.models.domain import Movie

class MovieRepository(ABC):
    @abstractmethod
    async def list_movies(self) -> List[Movie]: ...