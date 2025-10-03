from neo4j import AsyncGraphDatabase


class Neo4jMovieRepository:
    def __init__(self, uri=None, user=None, password=None):
        # … your existing init …
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def list_movies(self):
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (m:Movie)
                RETURN
                  m.id   AS id,
                  m.title AS title,
                  m.year  AS year,
                  m.genre AS genre
                """
            )
            # Async list comprehension to gather all records
            movies = [record.data() async for record in result]
            return movies

    async def close(self):
        await self.driver.close()