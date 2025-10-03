from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

from sqlalchemy.orm import relationship

class MovieORM(Base):
    __tablename__ = "movies"
    id = Column(String, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    genre = Column(String)

    reviews = relationship("ReviewORM", back_populates="movie", lazy="selectin")
    actors = relationship(
        "ActorORM",
        secondary="movie_actors",
        back_populates="movies",
        lazy="selectin"
    )

class ActorORM(Base):
    __tablename__ = "actors"
    id = Column(String, primary_key=True)
    name = Column(String)

    movies = relationship(
        "MovieORM",
        secondary="movie_actors",
        back_populates="actors",
        lazy="selectin"
    )


class MovieActorORM(Base):
    __tablename__ = "movie_actors"
    movie_id = Column(String, ForeignKey("movies.id"), primary_key=True)
    actor_id = Column(String, ForeignKey("actors.id"), primary_key=True)

class ReviewORM(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String, ForeignKey("movies.id"))
    user = Column(String)
    score = Column(Integer)
    comment = Column(String)

    movie = relationship("MovieORM", back_populates="reviews")
