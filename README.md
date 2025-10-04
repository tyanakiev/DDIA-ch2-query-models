DDIA-ch2-polyglot-movies

A hands-on exploration of Chapter 2: Data Models and Query Languages from Designing Data-Intensive Applications.
This project models a unified movie universe across three distinct databases—PostgreSQL, MongoDB, and Neo4j—
to compare how relational, document, and graph models shape data access, performance, and flexibility.

Purpose
-------
This repo is a practical playground for understanding:
- How different data models represent the same domain
- How query languages affect expressiveness and performance
- How to design modular, pluggable repositories for polyglot persistence
- How to seed, query, and benchmark across SQL, NoSQL, and graph databases

Architecture Overview
---------------------
FastAPI
│
├── SQL: PostgreSQL (movies, actors, reviews)
├── NoSQL: MongoDB (embedded reviews, flexible schema)
└── Graph: Neo4j (actor-movie relationships)

Each backend is accessed via a dedicated repository and exposed through clean REST endpoints.

Features
--------
- Bulk data seeding across all three databases
- Modular repository pattern with dependency injection
- REST API endpoints for each datastore
- Async I/O with Motor (Mongo) and Neo4j driver
- Unified domain model with Pydantic schemas
- Docker Compose setup for local development

Installation
------------
git clone https://github.com/tyanakiev/DDIA-ch2-polyglot-movies.git
cd DDIA-ch2-polyglot-movies
python -m venv venv
source venv/bin/activate  (or venv\Scripts\activate on Windows)
pip install -r requirements.txt

Run with Docker
---------------
docker-compose up -d

Services:
- postgres: relational backend
- mongo: document backend
- neo4j: graph backend
- fastapi: API layer

Seed the Databases
------------------
python -m app.scripts.seed_data

This populates each datastore with synthetic movie data using faker.

API Endpoints
-------------
GET /sql/movies     → List movies from PostgreSQL
GET /mongo/movies   → List movies from MongoDB
GET /neo4j/movies   → List movies from Neo4j

Chapter Connection
------------------
This project embodies Chapter 2 of Designing Data-Intensive Applications by:
- Modeling the same domain across relational, document, and graph paradigms
- Comparing query expressiveness and performance
- Exploring schema flexibility, joins vs. embedding, and traversal patterns

Future Directions
-----------------
- Unified endpoint stitching data from all three sources
- Benchmarking query latency and throughput
- GraphQL layer for flexible querying
- Observability with OpenTelemetry
- End-to-end tests with seeded data

Contributing
------------
Pull requests welcome! This repo is a learning lab—feel free to fork, extend, and experiment.

License
-------
MIT License. See LICENSE file for details.
