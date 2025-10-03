from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.future import select
from app.models.orm import MovieORM, ActorORM, MovieActorORM, ReviewORM
from app.models.domain import Movie, Actor, Review
from app.repositories.base import MovieRepository

class SQLMovieRepository(MovieRepository):
    def __init__(self, dsn: str):
        self.engine = create_async_engine(dsn, echo=True)
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def list_movies(self) -> list[Movie]:
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(MovieORM).options(selectinload(MovieORM.reviews))
            )
            movies = result.scalars().all()
            return [Movie(
                id=m.id,
                title=m.title,
                year=m.year,
                genre=m.genre,
                actors=[],  # Add actor loading later
                reviews=[]  # Add review loading later
            ) for m in movies]