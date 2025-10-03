from fastapi import Depends
from app.config     import settings
from app.repositories.sql_repo   import SQLMovieRepository
from app.repositories.mongo_repo import MongoMovieRepository
from app.repositories.neo4j_repo import Neo4jMovieRepository
from app.repositories.base       import MovieRepository

def get_sql_repo() -> MovieRepository:
    return SQLMovieRepository(settings.POSTGRES_DSN)

def get_mongo_repo():
    return MongoMovieRepository(settings.MONGO_URI, settings.MONGO_DB)


def get_neo4j_repo():
    return Neo4jMovieRepository(
        settings.NEO4J_URI,
        settings.NEO4J_USER,
        settings.NEO4J_PASS
    )

def get_repo(namespace: str = Depends()) -> MovieRepository:
    if namespace == "sql":
        return get_sql_repo()
    if namespace == "mongo":
        return get_mongo_repo()
    if namespace == "neo4j":
        return get_neo4j_repo()
    raise ValueError("Unknown namespace")