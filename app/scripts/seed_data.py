import asyncio
from faker import Faker
from typing import List
from sqlalchemy import select
# SQLAlchemy imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# MongoDB imports
from motor.motor_asyncio import AsyncIOMotorClient

# Neo4j imports
from neo4j import AsyncGraphDatabase

# Your app’s modules
from app.config import settings
from app.models.orm import Base, MovieORM, ReviewORM, ActorORM, MovieActorORM

fake = Faker()

# Number of movies to generate
NUM_MOVIES = 100

async def seed_postgres():
    engine = create_async_engine(settings.POSTGRES_DSN, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        for _ in range(NUM_MOVIES):
            movie_id = fake.uuid4()
            movie = MovieORM(
                id=movie_id,
                title=fake.sentence(nb_words=3),
                year=int(fake.year()),

                genre=fake.word(ext_word_list=["Drama","Comedy","Action","Sci-Fi","Horror"])
            )
            session.add(movie)
            await session.flush()

            # Reviews
            for _ in range(5):
                review = ReviewORM(
                    movie_id=movie_id,
                    user=fake.user_name(),
                    score=fake.random_int(min=1, max=10),
                    comment=fake.sentence()
                )
                session.add(review)

            # Actors (3 per movie, reuse or create)
            actor_names = [fake.name() for _ in range(3)]
            for name in actor_names:
                actor = await session.scalar(
                    select(ActorORM).filter_by(name=name)
                )

                if not actor:
                    actor = ActorORM(id=fake.uuid4(), name=name)
                    session.add(actor)
                    await session.flush()

                assoc = MovieActorORM(movie_id=movie_id, actor_id=actor.id)
                session.add(assoc)

        await session.commit()
    await engine.dispose()

async def seed_mongo():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB]

    movies_coll = db.get_collection("movies")

    bulk = []
    for _ in range(NUM_MOVIES):
        movie_id = fake.uuid4()
        doc = {
            "_id": movie_id,
            "title": fake.sentence(nb_words=3),
            "year": int(fake.year()),
            "genre": fake.word(ext_word_list=["Drama","Comedy","Action","Sci-Fi","Horror"]),
            "reviews": [
                {"user": fake.user_name(), "score": fake.random_int(1,10), "comment": fake.sentence()}
                for __ in range(5)
            ],
            "actors": [fake.name() for __ in range(3)]
        }
        bulk.append(doc)

    if bulk:
        await movies_coll.insert_many(bulk)
    client.close()

async def seed_neo4j():
    driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASS)
    )
    async with driver:
        async with driver.session() as session:
            for _ in range(NUM_MOVIES):
                movie_id = fake.uuid4()
                title = fake.sentence(nb_words=3)
                year = int(fake.year())
                genre = fake.word(ext_word_list=["Drama","Comedy","Action","Sci-Fi","Horror"])
                reviews = [
                    {"user": fake.user_name(), "score": fake.random_int(1,10), "comment": fake.sentence()}
                    for __ in range(5)
                ]
                actors = [fake.name() for __ in range(3)]

                # Create movie node
                await session.run(
                    """
                    CREATE (m:Movie {id: $id, title: $title, year: $year, genre: $genre})
                    """,
                    {"id": movie_id, "title": title, "year": year, "genre": genre}
                )

                # Create review nodes & relationships
                for rev in reviews:
                    await session.run(
                        """
                        MATCH (m:Movie {id: $id})
                        CREATE (r:Review {user: $user, score: $score, comment: $comment})
                        CREATE (r)-[:REVIEWS]->(m)
                        """,
                        {"id": movie_id, **rev}
                    )

                # Create actor nodes & relationships
                for name in actors:
                    await session.run(
                        """
                        MERGE (a:Actor {name: $name})
                        WITH a
                        MATCH (m:Movie {id: $id})
                        MERGE (a)-[:ACTED_IN]->(m)
                        """,
                        {"name": name, "id": movie_id}
                    )
    await driver.close()

async def main():
    # Run each seeder in series
    await seed_postgres()
    await seed_mongo()
    await seed_neo4j()

if __name__ == "__main__":
    asyncio.run(main())