from sqlalchemy import create_engine
from neo4j import GraphDatabase

POSTGRES_URL = "postgresql://user_tcc:password_tcc@localhost:5432/movielens_db"
postgres_engine = create_engine(POSTGRES_URL)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "password_tcc")
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)


def get_postgres_connection():
    return postgres_engine.connect()


def get_neo4j_session():
    return neo4j_driver.session()
