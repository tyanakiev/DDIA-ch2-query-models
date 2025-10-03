from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DSN: str = "postgresql+asyncpg://user:newpass@localhost:5432/movies"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "movies"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASS: str = "passpasspass"

settings = Settings()
