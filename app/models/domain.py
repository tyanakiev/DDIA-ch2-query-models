from pydantic import BaseModel
from typing import List

class Actor(BaseModel):
    id: str
    name: str

class Review(BaseModel):
    user: str
    score: float
    comment: str

class Movie(BaseModel):
    id: str
    title: str
    year: int
    genre: str
    actors: List[Actor] = []
    reviews: List[Review] = []