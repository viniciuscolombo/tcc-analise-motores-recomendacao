import pandas as pd
from neo4j import GraphDatabase
from etl_process import extract_and_transform

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password_tcc")

def load_to_neo4j():
    movies_df, ratings_df, filme_genero_df, generos_df = extract_and_transform()
    
    print("\n3. Conectando ao banco Neo4j")
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    with driver.session() as session:
        print(" -> Criando índices de performance")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieId IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE")
        
        print(" -> Inserindo Nós de Filmes...")
        movies_dict = movies_df[['movieId', 'title']].to_dict('records')
        session.run("""
            UNWIND $movies AS m
            MERGE (movie:Movie {movieId: m.movieId})
            SET movie.title = m.title
        """, movies=movies_dict)
        
        print(" -> Inserindo Nós de Gêneros e criando Relacionamentos")
        genres_dict = filme_genero_df[['movieId', 'genre']].to_dict('records')
        session.run("""
            UNWIND $genres AS g
            MATCH (m:Movie {movieId: g.movieId})
            MERGE (gen:Genre {name: g.genre})
            MERGE (m)-[:IN_GENRE]->(gen)
        """, genres=genres_dict)
        
        print(" -> Inserindo Avaliações")
        ratings_dict = ratings_df[['userId', 'movieId', 'rating']].to_dict('records')
        session.run("""
            UNWIND $ratings AS r
            MERGE (u:User {userId: r.userId})
            WITH u, r
            MATCH (m:Movie {movieId: r.movieId})
            MERGE (u)-[rel:RATED]->(m)
            SET rel.rating = r.rating
        """, ratings=ratings_dict)
        
    driver.close()
    print("\nSucesso! Carga no Neo4j concluída. O banco de grafos está populado.")

if __name__ == "__main__":
    load_to_neo4j()