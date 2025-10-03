from fastapi import FastAPI
from app.api import sql_routes, mongo_routes, neo4j_routes

app = FastAPI(title="Movie Universe Explorer")

app.include_router(sql_routes.router,    prefix="/sql",    tags=["sql"])
app.include_router(mongo_routes.router,  prefix="/mongo",  tags=["mongo"])
app.include_router(neo4j_routes.router,  prefix="/neo4j",  tags=["neo4j"])